from db import get_db
from bson.objectid import ObjectId
from datetime import datetime

# -------------------------------
# FUNCIONES AUXILIARES INTERNAS
# -------------------------------

def _buscar_funcion_por_hora(funciones, hora_funcion):
    """Devuelve la función que coincide con la hora especificada."""
    return next((f for f in funciones if f["hora"] == hora_funcion), None)

def _actualizar_disponibilidad(peliculas, id_pelicula, funciones, hora_funcion, cantidad):
    """Resta la cantidad de entradas disponibles para una función específica."""
    for f in funciones:
        if f["hora"] == hora_funcion:
            f["disponibles"] -= cantidad
            break
    peliculas.update_one(
        {"_id": ObjectId(id_pelicula)},
        {"$set": {"funciones": funciones}}
    )

def _registrar_compra(entradas, id_usuario, id_pelicula, hora_funcion, cantidad):
    """Guarda la compra en la colección de entradas."""
    compra = {
        "id_usuario": ObjectId(id_usuario),
        "id_pelicula": ObjectId(id_pelicula),
        "hora_funcion": hora_funcion,
        "cantidad": cantidad,
        "fecha_compra": datetime.now()
    }
    return entradas.insert_one(compra)

def _agregar_a_historial_usuario(usuarios, id_usuario, id_entrada):
    """Agrega el ID de la entrada al historial de compras del usuario."""
    usuarios.update_one(
        {"_id": ObjectId(id_usuario)},
        {"$push": {"historial_compras": id_entrada}}
    )

# -------------------------------
# FUNCIONES PRINCIPALES
# -------------------------------

def obtener_pelicula_por_id(id_pelicula):
    """Devuelve una película según su ID."""
    db = get_db()
    return db.peliculas.find_one({"_id": ObjectId(id_pelicula)})

def comprar_entrada(id_usuario, id_pelicula, hora_funcion, cantidad=1):
    """
    Intenta comprar 'cantidad' entradas para la película y función indicada.
    Verifica disponibilidad, actualiza inventario y registra la compra.
    """
    db = get_db()
    peliculas = db.peliculas
    usuarios = db.usuarios
    entradas = db.entradas

    pelicula = peliculas.find_one({"_id": ObjectId(id_pelicula)})
    if not pelicula:
        return False, "Película no encontrada"

    funciones = pelicula.get("funciones", [])
    funcion_obj = _buscar_funcion_por_hora(funciones, hora_funcion)

    if not funcion_obj:
        return False, "Función no encontrada"

    if funcion_obj["disponibles"] < cantidad:
        return False, "No hay suficientes entradas disponibles"

    # Actualiza la disponibilidad de entradas
    _actualizar_disponibilidad(peliculas, id_pelicula, funciones, hora_funcion, cantidad)

    # Registra la compra
    resultado = _registrar_compra(entradas, id_usuario, id_pelicula, hora_funcion, cantidad)

    # Agrega la compra al historial del usuario
    _agregar_a_historial_usuario(usuarios, id_usuario, resultado.inserted_id)

    return True, f"Compra exitosa. ID: {resultado.inserted_id}"

def obtener_historial_usuario(id_usuario):
    """
    Devuelve una lista de compras realizadas por el usuario.
    Cada entrada incluye el nombre de la película, hora, cantidad y fecha.
    """
    db = get_db()
    usuarios = db.usuarios
    entradas = db.entradas
    peliculas = db.peliculas

    user = usuarios.find_one({"_id": ObjectId(id_usuario)})
    if not user or "historial_compras" not in user:
        return []

    historial_detalles = []

    for entrada_id in user["historial_compras"]:
        entrada = entradas.find_one({"_id": entrada_id})
        if entrada:
            pelicula = peliculas.find_one({"_id": entrada["id_pelicula"]})
            historial_detalles.append({
                "pelicula": pelicula["nombre"] if pelicula else "Desconocida",
                "funcion": entrada["hora_funcion"],
                "cantidad": entrada["cantidad"],
                "fecha": entrada["fecha_compra"]
            })

    return historial_detalles

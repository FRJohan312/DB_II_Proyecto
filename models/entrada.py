from db import get_db
from bson.objectid import ObjectId
from datetime import datetime

def obtener_pelicula_por_id(id_pelicula):
    db = get_db()
    return db.peliculas.find_one({"_id": ObjectId(id_pelicula)})

def comprar_entrada(id_usuario, id_pelicula, hora_funcion, cantidad=1):
    """
    Intenta comprar 'cantidad' entradas para la película y función indicada.
    Actualiza el inventario y registra la compra en la colección 'usuarios'.
    """
    db = get_db()
    peliculas = db.peliculas
    usuarios = db.usuarios
    entradas = db.entradas  # colección para guardar compras

    pelicula = peliculas.find_one({"_id": ObjectId(id_pelicula)})
    if not pelicula:
        return False, "Película no encontrada"

    # Buscar la función con esa hora
    funciones = pelicula.get("funciones", [])
    funcion_obj = None
    for f in funciones:
        if f["hora"] == hora_funcion:
            funcion_obj = f
            break
    if not funcion_obj:
        return False, "Función no encontrada"

    if funcion_obj["disponibles"] < cantidad:
        return False, "No hay suficientes entradas disponibles"

    # Actualizar disponibilidad de la función
    nuevas_funciones = []
    for f in funciones:
        if f["hora"] == hora_funcion:
            f["disponibles"] -= cantidad
        nuevas_funciones.append(f)

    peliculas.update_one(
        {"_id": ObjectId(id_pelicula)},
        {"$set": {"funciones": nuevas_funciones}}
    )

    # Registrar compra en colección entradas
    compra = {
        "id_usuario": ObjectId(id_usuario),
        "id_pelicula": ObjectId(id_pelicula),
        "hora_funcion": hora_funcion,
        "cantidad": cantidad,
        "fecha_compra": datetime.now()
    }
    resultado = entradas.insert_one(compra)

    # Actualizar historial de compras en usuario (opcional)
    usuarios.update_one(
        {"_id": ObjectId(id_usuario)},
        {"$push": {"historial_compras": resultado.inserted_id}}
    )

    return True, f"Compra exitosa. ID: {resultado.inserted_id}"

def obtener_historial_usuario(id_usuario):
    db = get_db()
    usuarios = db.usuarios
    entradas = db.entradas
    peliculas = db.peliculas

    user = usuarios.find_one({"_id": ObjectId(id_usuario)})
    if not user or "historial_compras" not in user:
        return []

    historial_ids = user["historial_compras"]
    historial_detalles = []

    for entrada_id in historial_ids:
        entrada = entradas.find_one({"_id": entrada_id})
        if entrada:
            pelicula = peliculas.find_one({"_id": entrada["id_pelicula"]})
            historial_detalles.append({
                "pelicula": pelicula["nombre"] if pelicula else "Desconocida",
                "hora_funcion": entrada["hora_funcion"],
                "cantidad": entrada["cantidad"],
                "fecha_compra": entrada["fecha_compra"]
            })

    return historial_detalles

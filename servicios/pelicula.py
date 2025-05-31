from db import get_db
from bson.objectid import ObjectId

# -------------------------------
# FUNCIONES AUXILIARES INTERNAS
# -------------------------------

def _get_peliculas_collection():
    """Devuelve la colección de películas desde la base de datos."""
    db = get_db()
    return db.peliculas

# -------------------------------
# FUNCIONES PRINCIPALES
# -------------------------------

def agregar_pelicula(nombre, genero, duracion, funciones):
    """
    Inserta una nueva película en la base de datos.
    
    Parámetros:
        - nombre (str): Nombre de la película.
        - genero (str): Género de la película.
        - duracion (int): Duración en minutos.
        - funciones (list): Lista de funciones, cada una con hora y cupo disponible.
          Ejemplo: [{"hora": "18:00", "disponibles": 80}, ...]
    
    Retorna:
        - True si la película se insertó correctamente.
    """
    peliculas = _get_peliculas_collection()

    pelicula = {
        "nombre": nombre,
        "genero": genero,
        "duracion": duracion,
        "funciones": funciones
    }

    resultado = peliculas.insert_one(pelicula)
    print("Película insertada con ID:", resultado.inserted_id)
    return True

def obtener_peliculas():
    """
    Retorna una lista con todas las películas almacenadas en la base de datos.
    """
    peliculas = _get_peliculas_collection()
    return list(peliculas.find())

def eliminar_pelicula(id_pelicula):
    """
    Elimina una película según su ID.
    
    Parámetros:
        - id_pelicula (str): ID de la película en formato string.
    
    Retorna:
        - True si se eliminó correctamente, False si no se encontró.
    """
    peliculas = _get_peliculas_collection()
    resultado = peliculas.delete_one({"_id": ObjectId(id_pelicula)})
    return resultado.deleted_count > 0

def editar_pelicula(id_pelicula, nombre, genero, duracion, funciones):
    """
    Edita los datos de una película existente.
    
    Parámetros:
        - id_pelicula (str): ID de la película.
        - nombre (str), genero (str), duracion (int), funciones (list): Nuevos datos.
    
    Retorna:
        - True si la película fue modificada correctamente.
    """
    peliculas = _get_peliculas_collection()

    resultado = peliculas.update_one(
        {"_id": ObjectId(id_pelicula)},
        {
            "$set": {
                "nombre": nombre,
                "genero": genero,
                "duracion": duracion,
                "funciones": funciones
            }
        }
    )
    return resultado.modified_count > 0

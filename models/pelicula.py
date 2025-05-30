from db import get_db
from bson.objectid import ObjectId

def agregar_pelicula(nombre, genero, duracion, funciones):
    """
    Inserta una nueva película en la base de datos.
    - funciones debe ser una lista de diccionarios: [{"hora": "18:00", "disponibles": 80}, ...]
    """
    db = get_db()
    peliculas = db.peliculas

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
    db = get_db()
    peliculas = db.peliculas
    return list(peliculas.find())


def eliminar_pelicula(id_pelicula):
    db = get_db()
    peliculas = db.peliculas
    resultado = peliculas.delete_one({"_id": ObjectId(id_pelicula)})
    return resultado.deleted_count > 0

def editar_pelicula(id_pelicula, nombre, genero, duracion, funciones):
    db = get_db()
    peliculas = db.peliculas
    resultado = peliculas.update_one(
        {"_id": ObjectId(id_pelicula)},
        {"$set": {
            "nombre": nombre,
            "genero": genero,
            "duracion": duracion,
            "funciones": funciones
        }}
    )
    return resultado.modified_count > 0

from db import get_db
from bson import ObjectId

db = get_db()
usuarios = db["usuarios"]

def registrar_usuario(nombre, correo, preferencias):
    db = get_db()
    usuarios = db.usuarios

    usuario = {
        "nombre": nombre,
        "correo": correo,
        "historial_compras": [],
        "preferencias": preferencias  # ahora sí lo recibimos
    }

    result = usuarios.insert_one(usuario)
    print("Usuario insertado con ID:", result.inserted_id)

    return result.inserted_id


def obtener_usuarios():
    db = get_db()
    usuarios = db.usuarios.find()
    return list(usuarios)

def obtener_historial(usuario_id):
    db = get_db()
    usuario = db.usuarios.find_one({"_id": ObjectId(usuario_id)})
    if usuario and "historial" in usuario:
        return usuario["historial"]
    return []
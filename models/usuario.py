from bson import ObjectId
from db import get_db
import bcrypt
from db import get_db

def registrar_usuario(nombre, correo, contraseña, preferencias, rol):
    db = get_db()
    usuarios = db.usuarios

    if usuarios.find_one({"correo": correo}):
        return None
    
    password_encriptada = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

    usuario = {
        "nombre": nombre,
        "correo": correo,
        "contraseña": password_encriptada,
        "historial_compras": [],
        "preferencias": preferencias,
        "rol": rol
    }

    result = usuarios.insert_one(usuario)
    return result.inserted_id

def obtener_usuario_por_correo(correo):
    db = get_db()
    return db.usuarios.find_one({"correo": correo})

def obtener_usuarios():
    db = get_db()
    return list(db.usuarios.find())

def obtener_historial(usuario_id):
    db = get_db()
    usuario = db.usuarios.find_one({"_id": ObjectId(usuario_id)})
    if usuario and "historial" in usuario:
        return usuario["historial"]
    return []

def verificar_credenciales(correo, contraseña):
    db = get_db()
    usuario = db.usuarios.find_one({"correo": correo})
    
    if usuario and bcrypt.checkpw(contraseña.encode('utf-8'), usuario["contraseña"]):
        return usuario  # Login correcto
    return None  # Falló la verificación
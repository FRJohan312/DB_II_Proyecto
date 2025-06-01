from bson import ObjectId
from db import get_db
import bcrypt
from .entrada import obtener_historial_usuario

# -------------------------------
# FUNCIONES AUXILIARES
# -------------------------------

def obtener_coleccion_usuarios():
    """Devuelve la colección de usuarios desde la base de datos."""
    db = get_db()
    return db.usuarios

# -------------------------------
# FUNCIONES PRINCIPALES DE USUARIO
# -------------------------------

def registrar_usuario(nombre, correo, contraseña, preferencias, rol):
    """
    Registra un nuevo usuario si el correo no está en uso.

    Parámetros:
        - nombre (str): Nombre completo del usuario.
        - correo (str): Correo único.
        - contraseña (str): Contraseña sin encriptar.
        - preferencias (list): Lista de géneros preferidos.
        - rol (str): 'admin' o 'usuario'.

    Retorna:
        - ID del usuario registrado (ObjectId) o None si el correo ya existe.
    """
    usuarios = obtener_coleccion_usuarios()

    if usuarios.find_one({"correo": correo}):
        return None  # El correo ya está registrado

    password_encriptada = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

    nuevo_usuario = {
        "nombre": nombre,
        "correo": correo,
        "contraseña": password_encriptada,
        "historial_compras": [],
        "preferencias": preferencias,
        "rol": rol
    }

    result = usuarios.insert_one(nuevo_usuario)
    return result.inserted_id

def obtener_usuario_por_correo(correo):
    """
    Retorna el usuario con el correo especificado, o None si no existe.
    """
    usuarios = obtener_coleccion_usuarios()
    return usuarios.find_one({"correo": correo})

def obtener_usuarios():
    """
    Retorna una lista con todos los usuarios registrados.
    """
    usuarios = obtener_coleccion_usuarios()
    return list(usuarios.find())

def actualizar_usuario(usuario_id, nombre, preferencias, rol):
    """
    Actualiza los datos básicos de un usuario (nombre, preferencias, rol).

    Parámetros:
        - usuario_id (str): ID del usuario en formato string.
        - nombre (str): Nuevo nombre.
        - preferencias (list): Lista de géneros preferidos.
        - rol (str): Nuevo rol.

    Retorna:
        - True si la actualización fue exitosa.
    """
    usuarios = obtener_coleccion_usuarios()

    resultado = usuarios.update_one(
        {"_id": ObjectId(usuario_id)},
        {"$set": {
            "nombre": nombre,
            "preferencias": preferencias,
            "rol": rol
        }}
    )
    return resultado.modified_count > 0

def eliminar_usuario(usuario_id):
    """
    Elimina un usuario por su ID.

    Retorna:
        - True si se eliminó correctamente.
    """
    usuarios = obtener_coleccion_usuarios()
    resultado = usuarios.delete_one({"_id": ObjectId(usuario_id)})
    return resultado.deleted_count > 0

def verificar_credenciales(correo, contraseña):
    """
    Verifica si el correo y contraseña coinciden con un usuario registrado.

    Retorna:
        - Diccionario del usuario si las credenciales son válidas, o None si fallan.
    """
    usuarios = obtener_coleccion_usuarios()
    usuario = usuarios.find_one({"correo": correo})
    
    if usuario and bcrypt.checkpw(contraseña.encode('utf-8'), usuario["contraseña"]):
        return usuario
    return None

def obtener_historial(usuario_id):
    """
    Retorna el historial de compras del usuario utilizando la lógica de entradas.
    """
    return obtener_historial_usuario(usuario_id)

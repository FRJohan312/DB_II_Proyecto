from pymongo import MongoClient
contrasena = "3jrpw5tmzRp9l40b"
def get_db():
    client = MongoClient(f"mongodb+srv://johangomez1:{contrasena}@cluster0.hhohkzv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    return client["DB_II_Proyecto"]

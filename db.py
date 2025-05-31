from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

contrasena = os.getenv("password")

def get_db():
    client = MongoClient(f"mongodb+srv://johangomez1:{contrasena}@cluster0.hhohkzv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    return client["DB_II_Proyecto"]

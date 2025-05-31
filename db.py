from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("username")
contrasena = os.getenv("password")
DB_NAME = os.getenv("db")

def get_db():
    client = MongoClient(f"mongodb+srv://johangomez1:{contrasena}@cluster0.hhohkzv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    return client[DB_NAME]

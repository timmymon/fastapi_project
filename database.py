import mysql.connector
from mysql.connector import Error

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Cambia el usuario si es necesario
        password="",  # Cambia la contraseña si es necesario
        database="fastapi_db"
    )

from passlib.context import CryptContext
from pydantic import EmailStr
from models import UserCreate, UserOut, UserUpdate
from database import get_db_connection

# Configuración de la encriptación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_by_username(username: str):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    return cursor.fetchone()

def create_user(user: UserCreate):
    db = get_db_connection()
    cursor = db.cursor()
    hashed_password = get_password_hash(user.password)
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                   (user.username, user.email, hashed_password))
    db.commit()

def update_user(user_id: int, user: UserUpdate):
    db = get_db_connection()
    cursor = db.cursor()
    if user.password:
        hashed_password = get_password_hash(user.password)
        cursor.execute("UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s", 
                       (user.username, user.email, hashed_password, user_id))
    else:
        cursor.execute("UPDATE users SET username = %s, email = %s WHERE id = %s", 
                       (user.username, user.email, user_id))
    db.commit()

def delete_user(user_id: int):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    db.commit()

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from auth import create_user, update_user, delete_user, get_user_by_username
from models import UserCreate, UserUpdate, UserOut
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()
# Servir archivos estáticos (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_index():
    # Sirve el archivo index.html cuando se accede a la ruta raíz "/"
    with open("frontend/index.html") as f:
        return f.read()

@app.post("/users/", response_model=UserOut)
def create_new_user(user: UserCreate):
    db_user = get_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    create_user(user)
    return user

@app.put("/users/{user_id}", response_model=UserOut)
def update_user_info(user_id: int, user: UserUpdate):
    update_user(user_id, user)
    return {**user.dict(), "id": user_id}

@app.delete("/users/{user_id}")
def delete_user_info(user_id: int):
    delete_user(user_id)
    return {"message": "User deleted successfully"}

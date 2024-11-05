from pydantic import BaseModel
from typing import Optional

# Esquema para el usuario (entrada y salida)
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

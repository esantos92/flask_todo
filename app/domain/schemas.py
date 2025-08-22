from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TodoIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None

class TodoOut(TodoIn):
    id: int
    done: bool
    title: str
    description: Optional[str] = None
from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional, List
from pydantic import EmailStr

class UserBase(SQLModel):
    username: str = Field(unique=True)
    email: EmailStr = Field(unique=True)
    role: str = Field(default="user")

class User(UserBase, table=True):
    id: int = Field(primary_key=True)
    hashed_password: str
    refresh_token: Optional[str] = None
    created_at: datetime
    todo_list: Optional[List["TodoList"]] = Field(foreign_key="todo_lists.id")

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

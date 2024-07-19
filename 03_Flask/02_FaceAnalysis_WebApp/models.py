from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import BaseModel

class User(SQLModel, table=True):
    __table_args__ = {"extend_existing":True}
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    username: str
    role: str = Field(default="user")
    email: str
    password: bytes
    age: int
    country: str
    city: str
    join_time: datetime = Field(default_factory=datetime.now)

class Comment(SQLModel, table=True):
    __table_args__ = {"extend_existing":True}
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    services: str
    user_id: int = Field(foreign_key="user.id")


class Login_User(BaseModel):
    email: str
    password: str

class Register_User(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    age: str
    country: str
    city: str

class Submit_Comment(BaseModel):
    content: str

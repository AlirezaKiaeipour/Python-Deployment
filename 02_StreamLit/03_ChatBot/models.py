from typing import Optional
from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    __table_args__ = {"extend_existing":True}
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    username: str
    email: str
    password: str

    message: list["Message"] = Relationship(back_populates="user")


class Message(SQLModel, table=True):
    __table_args__ = {"extend_existing":True}
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    text: str
    user_id: int = Field(default=None, foreign_key="user.id")

    user: User = Relationship(back_populates="message")
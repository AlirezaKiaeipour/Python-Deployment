from typing import Optional
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    __table_args__ = {"extend_existing":True}
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    username: str
    email: str
    password: str

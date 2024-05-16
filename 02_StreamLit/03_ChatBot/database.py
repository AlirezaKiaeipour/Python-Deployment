from sqlmodel import Session, SQLModel, create_engine, select
from models import User, Message
import streamlit as st

@st.cache_resource
def connect_database():
    # engine = create_engine("sqlite:///database.db")
    engine = create_engine("postgresql://root:rPuC0vswgyuQDQBRrMYwQYqj@db-chatbot:5432/postgres")
    SQLModel.metadata.create_all(engine)
    return engine

def get_users():
    with Session(engine) as session:
        result = select(User)
        users = session.exec(result).all()
        return users

def insert_user(name, username, email, password):
    result = User(name=name, username=username, email=email, password=password)
    with Session(engine) as session:
        session.add(result)
        session.commit()

def check_user(username, email):
    with Session(engine) as session:
        result = select(User).where(User.username == username).where(User.email == email)
        user = session.exec(result).first()
        if user is None:
            return True
        
def get_user_id(username):
    with Session(engine) as session:
        result = select(User).where(User.username == username)
        user = session.exec(result).first()
        return user.id
         
def insert_message(type_message, text_message, user_id):
    result = Message(type=type_message, text=text_message, user_id=user_id)
    with Session(engine) as session:
        session.add(result)
        session.commit()

def get_message(id):
    with Session(engine) as session:
        result = select(Message).where(Message.user_id == id)
        message = session.exec(result).all()
        return message
    
engine = connect_database()

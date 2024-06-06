from sqlmodel import Session, SQLModel, create_engine, select
from models import User

engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

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
        
def get_username(email):
    with Session(engine) as session:
        result = select(User).where(User.email == email)
        user = session.exec(result).first()
        return user.username
    
def authentication(email, password):
    with Session(engine) as session:
        result = select(User).where(User.email == email).where(User.password == password)
        user = session.exec(result).first()
        if user:
            return True

from sqlmodel import Session, SQLModel, create_engine, select
from models import User

# engine = create_engine("postgresql://root:CST1RRO7BWXefjwhREV4pYQ2@db-faceanalysis:5432/postgres")
engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)

def insert_user(first_name, last_name, username, email, password, age, country, city, time):
    result = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password, age=age, country=country, city=city, join_time=time)
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
    
def get_password(email):
    with Session(engine) as session:
        result = select(User).where(User.email == email)
        user = session.exec(result).first()
        if user:
            return user.password
    
def authentication(email):
    with Session(engine) as session:
        result = select(User).where(User.email == email)
        user = session.exec(result).first()
        if user:
            return True

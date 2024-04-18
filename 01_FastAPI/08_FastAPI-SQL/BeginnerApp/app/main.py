from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, HTTPException, Depends

DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    yield db
    db.close()

@app.get("/users")
def get_user(id:int, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id==id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    return user

@app.post("/users")
def add_user(name:str, email:str, db:Session = Depends(get_db)):
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.delete("/users/{id}")
def delete_user(id:int, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id==id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    db.delete(user)
    db.commit()
    return "User Deleted"

@app.put("/users/{id}")
def edit_user(id:int, name:str, email:str, db:Session=Depends(get_db)):
    user = db.query(User).filter(User.id==id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    user.name = name
    user.email = email
    db.commit()
    db.refresh(user)
    return user

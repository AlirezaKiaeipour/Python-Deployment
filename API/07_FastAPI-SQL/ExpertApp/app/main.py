from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    yield db
    db.close()


@app.get("/students/{id}", response_model=schemas.Student)
def get_student_db(id:int, db:Session = Depends(get_db)):
    db_student = crud.get_student(db=db, id=id)
    return db_student


@app.get("/students", response_model=list[schemas.Student])
def get_student_all_db(db: Session = Depends(get_db)):
    db_students = crud.get_student_all(db)
    return db_students


@app.post("/students", response_model=schemas.Student)
def add_student_db(student: schemas.StudentCreate, db:Session = Depends(get_db)):
    db_student = crud.add_student(db=db, student=student)
    return db_student


@app.put("/students", response_model=schemas.Student)
def update_student_db(id:int, student: schemas.StudentCreate, db:Session = Depends(get_db)):
    db_student = crud.update_student(id=id, db=db, student=student)
    return db_student


@app.get("/courses/{id}", response_model=schemas.Course)
def get_course_db(id:int, db:Session = Depends(get_db)):
    db_course = crud.get_course(db=db,id=id)
    return db_course


@app.get("/courses", response_model=list[schemas.Course])
def get_course_all_db(db: Session = Depends(get_db)):
    db_courses = crud.get_course_all(db)
    return db_courses


@app.post("/courses", response_model=schemas.Course)
def add_course_db(id:int, course: schemas.CourseCreate, db:Session = Depends(get_db)):
    db_course = crud.add_course(db=db, course=course, id=id)
    return db_course


@app.put("/courses", response_model=schemas.Course)
def update_course_db(id:int, course: schemas.CourseCreate, db:Session = Depends(get_db)):
    db_course = crud.update_course(id=id, db=db, course=course)
    return db_course

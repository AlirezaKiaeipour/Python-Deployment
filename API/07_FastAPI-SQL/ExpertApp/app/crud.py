from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException


def get_student(db: Session, id: int):
    student =  db.query(models.Student).filter(models.Student.id == id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student Not Found")
    return student


def get_student_all(db: Session):
    students =  db.query(models.Student).all()
    return students


def get_course(db:Session, id:int):
    course = db.query(models.Course).filter(models.Course.id == id).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course Not Found")
    return course


def get_course_all(db: Session):
    courses =  db.query(models.Course).all()
    return courses


def add_student(db:Session, student: schemas.StudentCreate):
    db_student = models.Student(firstname=student.firstname, lastname=student.lastname, average=student.average, graduated=student.graduated)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def add_course(db:Session, course: schemas.CourseCreate, id:int):
    db_course = models.Course(name=course.name,unit=course.unit,owner_id=id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def update_student(id:int, db:Session, student: schemas.StudentCreate):
    db_student = db.query(models.Student).filter(models.Student.id==id).first()
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student Not Found")
    db_student.firstname = student.firstname
    db_student.lastname = student.lastname
    db_student.average = student.average
    db_student.graduated = student.graduated
    db.commit()
    db.refresh(db_student)
    return db_student


def update_course(id:int, db:Session, course: schemas.CourseCreate):
    db_course = db.query(models.Course).filter(models.Course.id==id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course Not Found")
    db_course.name = course.name
    db_course.unit = course.unit
    db.commit()
    db.refresh(db_course)
    return db_course

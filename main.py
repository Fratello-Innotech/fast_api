from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import Student
from schema import  StudentCreate, StudentUpdate, StudentPatch
app=FastAPI()
Base.metadata.create_all(bind=engine)
@app.post("/students/")
def create_student(
    student : StudentCreate,
    db: Session = Depends(get_db)):
    new_student = Student(name=student.name, email=student.email, course=student.course, password=student.password)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {"message":"Successfully Students Created", "data":new_student}


@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return {"message": "Successfully Students Fetched","data":students}


@app.get("/students/{student_id}")
def get_student_by_id(student_id:int,db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code = 404, detail="Student Not Found")
    return {"message":"Successfully Student Fetched", "data":student}


@app.put("/students/{student_id}")
def update_student(student_id:int, student_data: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise  HTTPException(status_code=404, detail="Student Not Found")
    student.name = student_data.name
    student.email = student_data.email
    student.course = student_data.course
    student.password = student_data.password
    db.commit()
    db.refresh(student)
    return {"message":"Successfully Student Update", "data":student}


@app.patch("/students/{student_id}")
def patch_student(student_id: int, student_data: StudentPatch, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Students Not Found")
    data = student_data.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return {"message":"Student Partially Update", "data": student}


@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student Not Found")
    db.delete(student)
    db.commit()
    return {"message": "Successfully Student Deleted"}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class StudentCreate(BaseModel):
    name: str
    age: int
    course: str

class Student(StudentCreate):
    id: int

class StudentUpdate(BaseModel):
    name: str
    age: int
    course: str

students = { # Think of 'students' as our temporary database. The key is the student ID: 1 → Ravi, 2 → Arun 
    1: {
        "id": 1,
        "name": "Ravi",
        "age": 21,
        "course": "Python"
    },
    2: {
        "id": 2,
        "name": "Arun",
        "age": 22,
        "course": "Java"
    }
}

# GET /
@app.get("/")
def home():
    return {"message": "Student Management API"}

# GET /students
@app.get("/students", response_model=list[Student])
def get_students():
    return list(students.values())

# GET /students/1
# GET /students/100 -> {"detail": "Student not found"}
@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return students[student_id]

@app.post(
    "/students",
    response_model=Student,
    status_code=201
)
def create_student(student: StudentCreate):
    new_id = max(students.keys(), default=0) + 1
    new_student = {
        "id": new_id,
        **student.model_dump()
    }
    students[new_id] = new_student
    return new_student

@app.put(
    "/students/{student_id}",
    response_model=Student
)
def update_student(
    student_id: int,
    student: StudentUpdate
):
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    students[student_id] = {
        "id": student_id,
        **student.model_dump()
    }

    return students[student_id]

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    del students[student_id]

    return {
        "message": "Student deleted successfully"
    }

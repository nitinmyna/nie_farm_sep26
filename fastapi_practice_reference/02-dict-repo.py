from fastapi import FastAPI, HTTPException

app = FastAPI()

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
@app.get("/students")
def get_students():
    return list(students.values())

# GET /students/1
# GET /students/100 -> {"detail": "Student not found"}
@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return students[student_id]
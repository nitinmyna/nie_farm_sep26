from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from pymongo import MongoClient
from bson import ObjectId
from typing import Optional


# ---------------------------------------------------------
# 1. FastAPI Application
# ---------------------------------------------------------

app = FastAPI(
    title="Student Management API",
    description="Student Management REST API using FastAPI and MongoDB",
    version="2.0.0"
)


# ---------------------------------------------------------
# 2. MongoDB Connection
# ---------------------------------------------------------

MONGO_URL = "mongodb://localhost:27017"

client = MongoClient(MONGO_URL)

db = client["student_management"]

students_collection = db["students"]


# ---------------------------------------------------------
# 3. Pydantic Models
# ---------------------------------------------------------

class StudentCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=50
    )

    age: int = Field(
        ge=5,
        le=100
    )

    course: str = Field(
        min_length=2,
        max_length=50
    )


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50
    )

    age: Optional[int] = Field(
        default=None,
        ge=5,
        le=100
    )

    course: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50
    )


class StudentResponse(BaseModel):
    id: str
    name: str
    age: int
    course: str


# ---------------------------------------------------------
# 4. Helper Function
# ---------------------------------------------------------

def student_helper(student) -> dict:
    """
    Convert MongoDB document into API response format.
    """

    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "age": student["age"],
        "course": student["course"]
    }


# ---------------------------------------------------------
# 5. Home API
# ---------------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Student Management API",
        "version": "2.0.0"
    }


# ---------------------------------------------------------
# 6. CREATE Student
# ---------------------------------------------------------

@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(student: StudentCreate):

    student_data = student.model_dump()

    result = students_collection.insert_one(student_data)

    created_student = students_collection.find_one(
        {"_id": result.inserted_id}
    )

    return student_helper(created_student)


# ---------------------------------------------------------
# 7. GET All Students
# ---------------------------------------------------------

@app.get(
    "/students",
    response_model=list[StudentResponse]
)
def get_students():

    students = students_collection.find()

    return [
        student_helper(student)
        for student in students
    ]


# ---------------------------------------------------------
# 8. GET Student by ID
# ---------------------------------------------------------

@app.get(
    "/students/{student_id}",
    response_model=StudentResponse
)
def get_student(student_id: str):

    # Validate MongoDB ObjectId

    if not ObjectId.is_valid(student_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid student ID"
        )

    student = students_collection.find_one(
        {"_id": ObjectId(student_id)}
    )

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return student_helper(student)


# ---------------------------------------------------------
# 9. UPDATE Student
# ---------------------------------------------------------

@app.put(
    "/students/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: str,
    student: StudentUpdate
):

    if not ObjectId.is_valid(student_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid student ID"
        )

    update_data = student.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )

    result = students_collection.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    updated_student = students_collection.find_one(
        {"_id": ObjectId(student_id)}
    )

    return student_helper(updated_student)


# ---------------------------------------------------------
# 10. DELETE Student
# ---------------------------------------------------------

@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_student(student_id: str):

    if not ObjectId.is_valid(student_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid student ID"
        )

    result = students_collection.delete_one(
        {"_id": ObjectId(student_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return None
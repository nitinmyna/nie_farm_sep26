from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from pymongo import MongoClient
from bson import ObjectId
from typing import Optional
from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone


# =========================================================
# 1. FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Student Management API",
    description="FastAPI + MongoDB + JWT Authentication + RBAC",
    version="3.0.0"
)


# =========================================================
# 2. MONGODB
# =========================================================

MONGO_URL = "mongodb://localhost:27017"

client = MongoClient(MONGO_URL)

db = client["student_management"]

students_collection = db["students"]
users_collection = db["users"]


# =========================================================
# 3. PASSWORD HASHING
# =========================================================

password_hash = PasswordHash.recommended()


# =========================================================
# 4. JWT CONFIGURATION
# =========================================================

SECRET_KEY = "StudentAppSecurityKey" # change-this-secret-key

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# =========================================================
# 5. OAUTH2
# =========================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)


# =========================================================
# 6. PYDANTIC MODELS
# =========================================================


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


class UserCreate(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=30
    )

    password: str = Field(
        min_length=6
    )

    role: int = Field(
        ge=1,
        le=3
    )



class TokenResponse(BaseModel):

    access_token: str
    token_type: str


# =========================================================
# 7. HELPER FUNCTIONS
# =========================================================


def student_helper(student) -> dict:

    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "age": student["age"],
        "course": student["course"]
    }


def user_helper(user) -> dict:

    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "role": user["role"]
    }


# =========================================================
# 8. CREATE JWT
# =========================================================


def create_access_token(username: str, role: int):

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "role": role,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# =========================================================
# 9. GET CURRENT USER
# =========================================================


def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")
        role = payload.get("role")

        if username is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = users_collection.find_one(
        {"username": username}
    )

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


# =========================================================
# 10. ROLE AUTHORIZATION
# =========================================================


def require_roles(*allowed_roles):

    def role_checker(
        current_user=Depends(get_current_user)
    ):

        if current_user["role"] not in allowed_roles:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )

        return current_user

    return role_checker


# =========================================================
# 11. HOME
# =========================================================


@app.get("/")
def home():

    return {
        "message": "Student Management API",
        "version": "3.0.0"
    }


# =========================================================
# 12. CREATE USER
# =========================================================
#
# For workshop/demo setup only.
# In a production application, this endpoint should
# itself be protected according to the required policy.
# =========================================================


@app.post("/users")
def create_user(user: UserCreate):

    existing_user = users_collection.find_one(
        {"username": user.username}
    )

    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    hashed_password = password_hash.hash(
        user.password
    )

    user_data = {
        "username": user.username,
        "password": hashed_password,
        "role": user.role
    }

    result = users_collection.insert_one(
        user_data
    )

    created_user = users_collection.find_one(
        {"_id": result.inserted_id}
    )

    return user_helper(created_user)


# =========================================================
# 13. LOGIN
# =========================================================


@app.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = users_collection.find_one(
        {"username": form_data.username}
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not password_hash.verify(
        form_data.password,
        user["password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token(
        user["username"],
        user["role"]
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =========================================================
# 14. GET ALL STUDENTS
# =========================================================

@app.get(
    "/students",
    response_model=list[StudentResponse]
)
def get_students(
    current_user=Depends(
        require_roles(1, 2, 3)
    )
):

    students = students_collection.find()

    return [
        student_helper(student)
        for student in students
    ]


# =========================================================
# 15. GET ONE STUDENT
# =========================================================

@app.get(
    "/students/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: str,
    current_user=Depends(
        require_roles(1, 2, 3)
    )
):

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


# =========================================================
# 16. CREATE STUDENT
# =========================================================

@app.post(
    "/students",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(
    student: StudentCreate,
    current_user=Depends(
        require_roles(1, 2, 3)
    )
):

    student_data = student.model_dump()

    result = students_collection.insert_one(
        student_data
    )

    created_student = students_collection.find_one(
        {"_id": result.inserted_id}
    )

    return student_helper(created_student)


# =========================================================
# 17. UPDATE STUDENT
# =========================================================

@app.put(
    "/students/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: str,
    student: StudentUpdate,
    current_user=Depends(
        require_roles(1, 2)
    )
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


# =========================================================
# 18. DELETE STUDENT
# =========================================================

@app.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_student(
    student_id: str,
    current_user=Depends(
        require_roles(1)
    )
):

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
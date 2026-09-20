# Steps
```
1. Goal 

Client
   ↓
FastAPI
   ↓
Student REST APIs
   ↓
Python Dictionary

2. API End Points 
| Method | URL              | Operation |
| ------ | ---------------- | --------- |
| POST   | `/students`      | Create    |
| GET    | `/students`      | Read all  |
| GET    | `/students/{id}` | Read one  |
| PUT    | `/students/{id}` | Update    |
| DELETE | `/students/{id}` | Delete    |

3. Create Project
Directory: "/student/server"

4. Create Virtual Environment # Not Mandatory
python -m venv venv

Activate it on Windows:
venv\Scripts\activate

You should see something like:
(venv) C:\...\student\server>

Below cmd takes snapshot:
pip freeze > requirements.txt

Then another developer can recreate the environment with:
pip install -r requirements.txt

5. Install FastAPI and Uvicorn
pip install fastapi uvicorn

To check:
pip list

You should see:
fastapi
uvicorn

To update pip: # if needed
python.exe -m pip install --upgrade pip

6. Code Below:
```  

```py
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Student Management API"}
```

```
7. Run the Application
uvicorn main:app --reload

Meaning:
uvicorn # Server
   ↓
main.py
   ↓
app object

Uvicorn running on http://127.0.0.1:8000

8. Open http://127.0.0.1:8000 in browser.

Expected response:
{
    "message": "Student Management API"
}

9. Open Swagger UI
http://127.0.0.1:8000/docs

You will see:
Student Management API

GET /

Click:

GET / → Try it out → Execute

You should get:

{
  "message": "Student Management API"
}

This is the first important FastAPI experience for students:
Python Function
      ↓
FastAPI Route
      ↓
HTTP Request
      ↓
JSON Response

10. Create the In-Memory Database
Now add a dictionary.
```


```python
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
```

```
10.1 Open Swagger UI
http://127.0.0.1:8000/docs

GET /
GET /students
GET /students/1
GET /students/100 

Try the above API End Points on Swagger.
```

```
11. Add Pydantic request models
```

```python
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
```

```
12. CRUD

Students now have:

| Method | Endpoint         | Purpose  |
| ------ | ---------------- | -------- |
| POST   | `/students`      | Create   |
| GET    | `/students`      | Read all |
| GET    | `/students/{id}` | Read one |
| PUT    | `/students/{id}` | Update   |
| DELETE | `/students/{id}` | Delete   |


Create:
POST /students
- Request:
{
    "name": "Kumar",
    "age": 23,
    "course": "FastAPI"
}
- Response:
{
    "id": 3,
    "name": "Kumar",
    "age": 23,
    "course": "FastAPI"
}

Update:
PUT /students/1
- Request:
{
    "name": "Ravi Kumar",
    "age": 22,
    "course": "FastAPI"
}
...

Delete:
PUT /students/3
...

And they have experienced:

HTTP
 ↓
FastAPI
 ↓
Pydantic
 ↓
Validation
 ↓
CRUD
 ↓
HTTPException
 ↓
Swagger
 ↓
Postman

13. pymongo based student management
pip install fastapi uvicorn pymongo
--04____.py--
Swagger...

14. authN/authD based student management
pip install fastapi uvicorn pymongo pyjwt pwdlib
pip install "pwdlib[argon2]"
pip install python-multipart
--05____.py--
Swagger...
create users in different roles
try GET /login
Authorize in swagger
Then try the resources
```
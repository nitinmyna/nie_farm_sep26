## 1. What is FastAPI?

**FastAPI** is a Python web framework used to build **APIs and backend applications**.

It is:

* Easy to learn
* Fast
* Based on Python
* Suitable for REST APIs
* Supports asynchronous programming
* Provides automatic API documentation

Built on top of **Starlette** (for web routing and async capabilities) and **Pydantic** (for data validation and serialization)

**Starlette** → A lightweight **ASGI web framework/toolkit** that provides the core web capabilities on which FastAPI is built.

Starlette provides the web application framework, while Uvicorn provides the server that runs that ASGI application.

```text
Browser
   ↓ HTTP
Uvicorn          ← ASGI Server
   ↓ ASGI
Starlette        ← Web Framework
   ↓
FastAPI          ← Built on Starlette
   ↓
Your API code
```

## 2. FastAPI vs Flask vs Django

| Feature | FastAPI | Flask | Django |
| --- | --- | --- | --- |
| **Type** | Micro-framework (API-focused) | Micro-framework (General) | Full-stack ("Batteries included") |
| **Async Support** | Native (ASGI-first) | Added later (WSGI-first) | Added later (WSGI/ASGI hybrid) |
| **Data Validation** | Built-in via Pydantic | Requires third-party tools | Built-in via Django Forms/DRF |
| **Auto API Docs** | Yes (Swagger / ReDoc) | No (requires plugins) | No (requires DRF plugins) |
| **Best For** | High-speed microservices & APIs | Small apps, quick prototypes | Complex, monolithic applications |


**FastAPI:** API-first and modern backend development

**Flask:** Small and flexible web applications

**Django:** Complete web framework with many built-in features

## 3. ASGI vs WSGI

These are interfaces between a Python application and a web server.

* **WSGI (Web Server Gateway Interface):** Synchronous standard (used by older Flask/Django). Processes one request per thread at a time. If a request waits on a database query, that worker thread is blocked.
* **ASGI (Asynchronous Server Gateway Interface):** Modern asynchronous standard. Handles thousands of concurrent connections (like WebSockets, long polling, and high-volume I/O) on a single thread using Python's `async`/`await` event loop.

FastAPI is an **ASGI framework**.

```text
Client
   ↓
Web Server
   ↓
ASGI
   ↓
FastAPI
   ↓
Application Code
```

## 4. FastAPI Architecture

A simple FastAPI application can be understood as:

```text
Client
  ↓
HTTP Request
  ↓
Uvicorn
  ↓
FastAPI
  ↓
Route
  ↓
Business Logic
  ↓
Database
  ↓
HTTP Response
  ↓
Client
```

For example:

```text
GET /users
     ↓
FastAPI route
     ↓
User service
     ↓
Database
     ↓
JSON response
```

When an incoming request reaches your application:

1. **Client Request** triggers the ASGI Server (**Uvicorn**).
2. **Starlette** handles the request routing, headers, and async connection management.
3. **Pydantic** validates query parameters, paths, and JSON request bodies against your type definitions.
4. **FastAPI Route Handler** executes your custom logic (database calls, business logic).
5. **Response Serialization** converts Python objects/dictionaries back into clean JSON and returns HTTP status codes.

## 5. Uvicorn

**Uvicorn** is an **ASGI web server**.

FastAPI is the application framework.

> Uvicorn is a lightning-fast **ASGI web server** implementation for Python, powered by `uvloop` and `httptools`.

Uvicorn runs the FastAPI application.

Think of it as:

```text
Browser
   ↓
Uvicorn
   ↓
FastAPI Application
```

Example:

```bash
uvicorn main:app --reload
```

Meaning:

* `main` → `main.py`
* `app` → FastAPI object
* `--reload` → automatically restart during development

* **uvloop** → A high-performance replacement for Python’s default `asyncio` event loop, built on `libuv`.
* **httptools** → A fast, low-level HTTP protocol parser used by Uvicorn to efficiently handle HTTP requests and responses.
* **`asyncio` event loop** → Manages and schedules asynchronous tasks and I/O operations in Python.
* **libuv** → A high-performance library that provides asynchronous I/O and event-loop functionality.
  * libuv is a cross-platform C library for asynchronous I/O and event-loop operations.
  * > libuv provides the low-level mechanism for handling many I/O operations efficiently without blocking the application.
  * It can handle operations such as: 🌐 Network I/O — TCP, UDP, sockets 📁 File-system operations ⏱️ Timers ⚙️ Asynchronous tasks 🔄 Event-loop management
  * The relationship is: Uvicorn -> uvloop -> libuv -> Operating System
  * Example: When FastAPI is waiting for a database or network operation, the event loop can handle other requests instead of simply waiting
* **HTTP protocol parser** → Reads raw HTTP data and converts it into structured requests/responses that an application can process.
* **HTTP request** → A message sent by a client to a server asking it to perform an operation or return data.
* **HTTP response** → A message sent by a server back to the client containing the result of the request.

## 6. Interactive API Documentation

One of FastAPI's useful features is **automatic API documentation**.

FastAPI generates automatic interactive documentation directly from your route definitions and Pydantic schemas:

* **Swagger UI:** Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to test endpoints directly from the browser with an interactive "Try it out" interface.
* **ReDoc:** Visit [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) for an alternative, highly readable specification view optimized for API consumers.

After starting the server, open:

```text
http://127.0.0.1:8000/docs
```

You will see **Swagger UI**.

You can:

* See available APIs
* See HTTP methods
* Enter parameters
* Execute APIs
* See responses

FastAPI also provides:

```text
http://127.0.0.1:8000/redoc
```

This provides another documentation interface called **ReDoc**.

### Simple flow

```text
Write Python Code
       ↓
Define FastAPI Route
       ↓
Run Uvicorn
       ↓
FastAPI creates API
       ↓
Automatic documentation
       ↓
/docs
```

## Key Takeaways

We should remember these **7 points**:

1. **FastAPI** → Python framework for building APIs.
2. **FastAPI is ASGI-based.**
3. **Uvicorn** → runs the FastAPI application.
4. `FastAPI()` → creates the application.
5. `@app.get()` → defines a GET API.
6. `uvicorn main:app --reload` → starts the development server.
7. `/docs` → provides interactive API documentation.

> **FastAPI defines the API, Uvicorn runs it, and `/docs` helps us test it.**

## 7. HTTP Fundamentals

**HTTP = HyperText Transfer Protocol**

It is the communication protocol used between a **client** and a **server**.

> HTTP (Hypertext Transfer Protocol) is the language clients (browsers, mobile apps) and servers use to talk to each other.

Example:

```text
React Application
       ↓
   HTTP Request
       ↓
    FastAPI
       ↓
   HTTP Response
       ↓
React Application
```

### HTTP Request

> **Request:** The client asks for something (contains a method, URL, headers, and sometimes a body).

A request usually contains:

* Method
* URL
* Headers
* Body

Example:

```text
GET /users/10
```

### HTTP Response

> **Response:** The server replies (contains a status code, headers, and usually data).

A response usually contains:

* Status code
* Headers
* Response body

Example:

```json
{
    "id": 10,
    "name": "Ravi"
}
```

## 8. GET, POST, PUT, PATCH, DELETE

HTTP methods tell the server **what operation we want to perform**.

| Method | Purpose               | Example          |
| ------ | --------------------- | ---------------- |
| GET    | Read data             | Get users        |
| POST   | Create data           | Create user      |
| PUT    | Replace/update data   | Update user      |
| PATCH  | Partially update data | Change user name |
| DELETE | Delete data           | Delete user      |

> These are HTTP "Methods" (or verbs) that define the action you want to perform:

* **GET:** Read/retrieve data (e.g., fetch a list of users).
* **POST:** Create new data (e.g., sign up a new user).
* **PUT:** Replace existing data entirely (e.g., update a whole user profile).
* **PATCH:** Update data partially (e.g., change just the user's password).
* **DELETE:** Remove data.
  
### Simple CRUD mapping

```text
CREATE  → POST
READ    → GET
UPDATE  → PUT / PATCH
DELETE  → DELETE
```

## 9. Path Operations

A **path operation** connects an HTTP method and URL to a Python function.

> In FastAPI, a "path" is the URL endpoint (e.g., `/users`), and an "operation" is the HTTP method. You connect paths to Python functions using decorators:

Example:

```python
@app.get("/users")
def get_users():
    return {"message": "All users"}
```

Here:

```text
GET + /users
      ↓
get_users()
```

Another example:

```python
@app.post("/users")
def create_user():
    return {"message": "User created"}
```

The same path can have different operations:

```text
GET  /users → get users
POST /users → create user
```

## 10. Path Parameters

A **path parameter** is a value included in the URL path.

> Variables embedded directly into the URL path. They are declared using curly braces `{}` and passed as arguments to your function. FastAPI automatically converts data types based on type hints.

Example:

```text
/users/101
```

Here `101` is the user ID.

FastAPI:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

Request:

```text
GET /users/101
```

Response:

```json
{
    "user_id": 101
}
```

### Important

```text
/users/{user_id}
         ↑
    Path parameter
```

FastAPI also converts and validates the type:

```python
user_id: int
```

So:

```text
/users/101    → valid
/users/abc    → validation error
```

## 11. Query Parameters

Query parameters are values sent after `?` in the URL.

> Key-value pairs added to the end of a URL after a `?` (e.g., `/items?skip=0&limit=10`). In FastAPI, if a function parameter is **not** part of the URL path, it is automatically treated as a query parameter.

Example:

```text
/users?city=Trichy
```

Here:

```text
city=Trichy
```

is a query parameter.

FastAPI:

```python
@app.get("/users")
def get_users(city: str):
    return {"city": city}
```

Request:

```text
GET /users?city=Trichy
```

Response:

```json
{
    "city": "Trichy"
}
```

### Multiple query parameters

```text
/users?city=Trichy&age=30
```

```python
@app.get("/users")
def get_users(city: str, age: int):
    return {
        "city": city,
        "age": age
    }
```

### Path vs Query

```text
/users/101
       ↑
     Path
```

```text
/users?city=Trichy
       ↑
     Query
```

**Path parameter** usually identifies a specific resource.

**Query parameter** usually filters or controls the request.


## 12. Request Body

The **request body** contains data sent to the server.

> Data sent by the client to your API (usually in JSON format), mostly used with `POST`, `PUT`, or `PATCH`. FastAPI uses **Pydantic** models to validate this data.

It is commonly used with:

```text
POST
PUT
PATCH
```

Example JSON:

```json
{
    "name": "Ravi",
    "age": 30
}
```

FastAPI can define the body using **Pydantic models**.

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
```

Then:

```python
@app.post("/users")
def create_user(user: User):
    return user
```

Request:

```text
POST /users
```

Body:

```json
{
    "name": "Ravi",
    "age": 30
}
```

FastAPI automatically:

* Reads the JSON
* Validates the data
* Converts it into a Python object


## 13. HTTP Status Codes

The server uses a **status code** to tell the client what happened.

> Three-digit numbers telling the client the result of their request.

### Common status codes

| Code | Meaning               |
| ---- | --------------------- |
| 200  | OK                    |
| 201  | Created               |
| 204  | No Content            |
| 400  | Bad Request           |
| 401  | Unauthorized          |
| 403  | Forbidden             |
| 404  | Not Found             |
| 500  | Internal Server Error |

* **2xx (Success):** `200 OK` (Standard success), `201 Created` (New resource made).
* **4xx (Client Error):** `400 Bad Request` (Invalid input), `401 Unauthorized` (Needs login), `404 Not Found` (URL doesn't exist).
* **5xx (Server Error):** `500 Internal Server Error` (Your code crashed).

> *FastAPI defaults to 200, but you can change it via `@app.post("/items/", status_code=201)`.*

### Examples

Successful GET:

```text
200 OK
```

Successful POST:

```text
201 Created
```

Resource doesn't exist:

```text
404 Not Found
```

Invalid request:

```text
400 Bad Request
```


## 14. Response Objects

FastAPI normally converts Python return values into JSON responses.

> FastAPI automatically converts your Python dicts, lists, strings, and Pydantic models into valid JSON responses. If you need fine-grained control, you can return a custom `Response` directly (like `JSONResponse`, `HTMLResponse`, or `FileResponse`).

Example:

```python
@app.get("/hello")
def hello():
    return {"message": "Hello"}
```

Response:

```json
{
    "message": "Hello"
}
```

We can also specify a status code.

```python
from fastapi import status

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user():
    return {"message": "User created"}
```

Response:

```text
201 Created
```

FastAPI also provides `JSONResponse` when we need more control.

```python
from fastapi.responses import JSONResponse

@app.get("/test")
def test():
    return JSONResponse(
        content={"message": "Hello"},
        status_code=200
    )
```

## 15. Headers

**Headers** contain additional information about an HTTP request or response.

> Headers pass extra metadata with requests or responses (like `User-Agent`, `Authorization`, or `Content-Type`).

Examples:

```text
Authorization
Content-Type
Accept
User-Agent
```

Example request:

```text
Authorization: Bearer abc123
```

FastAPI can read headers using `Header`.

```python
from fastapi import Header

@app.get("/hello")
def hello(user_agent: str | None = Header(default=None)): # Header(None)
    return {"user_agent": user_agent}
```

*(Note: FastAPI automatically converts HTTP headers like `User-Agent` to Python variables like `user_agent`).*

### Why are headers useful?

Headers are commonly used for:

* Authentication
* Content type
* Client information
* Caching
* API-related metadata

## 16. Cookies

A **cookie** is a small piece of data stored by the browser.

> Cookies store small pieces of data on the client's browser. You can read them similarly to headers by importing `Cookie`.

Example:

```text
session_id=ABC123
```

The browser sends the cookie with later requests.

### Reading a cookie

```python
from fastapi import Cookie

@app.get("/profile")
def profile(session_id: str | None = Cookie(default=None)):
    return {"session_id": session_id}
```

### Setting a cookie

```python
from fastapi import Response

@app.get("/login")
def login(response: Response):
    response.set_cookie(
        key="session_id",
        value="ABC123"
    )

    return {"message": "Logged in"}
```


## Key Takeaways
1. **HTTP** is used for client-server communication.
2. **GET** → read.
3. **POST** → create.
4. **PUT/PATCH** → update.
5. **DELETE** → remove.
6. **Path parameters** identify resources.
7. **Query parameters** filter/control requests.
8. **Request body** carries data to the server.
9. **Status codes** tell the client the result.
10. **Headers** carry additional request/response information.
11. **Cookies** store small pieces of client-side data.

> **Method tells what to do, path tells where, parameters provide values, body provides data, and status code tells the result.**

## 17. Python Type Hints

**Type hints** tell us what type of data a variable should contain.

> Type hints are a standard Python feature used to specify the expected data type of a variable, parameter, or return value. FastAPI uses them under the hood to automatically validate data and generate documentation.

```python
name: str = "Ravi"
age: int = 30
salary: float = 50000.0
active: bool = True
```

Function example:

```python
def add(a: int, b: int) -> int:
    return a + b
```

Type hints make code:

* Easier to understand
* Easier to maintain
* Easier to validate

FastAPI uses type hints heavily.

## 18. Pydantic Models

**Pydantic** is used to define and validate data.

> Pydantic is a library for data validation. You create a "model" by creating a class that inherits from `BaseModel`. You define the expected structure of your data using Python type hints.

Example:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
```

Now `User` describes the expected data:

```json
{
    "name": "Ravi",
    "age": 30
}
```

Pydantic checks whether the data matches the model.

## 19. Request Models

A request model describes the **data expected from the client**.

> When you pass a Pydantic model to a FastAPI path operation, it acts as a **Request Model**. FastAPI automatically reads the incoming JSON body, validates it against the model, and hands it to you as a Python object.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

@app.post("/users")
def create_user(user: User):
    return user
```

Client sends:

```json
{
    "name": "Ravi",
    "age": 30
}
```

FastAPI:

```text
JSON Request
     ↓
Pydantic Model
     ↓
Validation
     ↓
Python Object
     ↓
Function
```

## 20. Field Validation

We can add rules to fields.

> You can add stricter rules to your model fields (like minimum length, or greater than zero) using Pydantic's `Field` function.

Example:

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(min_length=3)
    age: int = Field(ge=18)
```

Here:

```text
min_length=3
```

means name must have at least 3 characters.

```text
ge=18
```

means age must be **greater than or equal to 18**.

Example:

```json
{
    "name": "R",
    "age": 15
}
```

This will fail validation.

## 21. Optional / Default Fields

Some fields may be optional.

> If a field isn't required, you can set a default value. If a field can be missing entirely, use the `| None` syntax (or `Optional` in older Python versions) with a default of `None`.

### Default value

```python
class User(BaseModel):
    name: str
    age: int = 18
```

If age is not provided:

```text
age = 18
```

is used.

### Optional field

```python
class User(BaseModel):
    name: str
    phone: str | None = None
```

`phone` can contain a string or `None`.

Example:

```json
{
    "name": "Ravi"
}
```

This is valid.

## 22. Nested Models

A Pydantic model can contain another Pydantic model.

> You can use a Pydantic model as a type hint inside *another* Pydantic model. This allows you to validate complex, multi-level JSON structures.

Example:

```python
class Address(BaseModel):
    city: str
    pincode: int

class User(BaseModel):
    name: str
    address: Address
```

Request:

```json
{
    "name": "Ravi",
    "address": {
        "city": "Trichy",
        "pincode": 620001
    }
}
```

Structure:

```text
User
 ├── name
 └── address
      ├── city
      └── pincode
```

This is useful for complex JSON data.


## 23. Lists and Dictionaries

Pydantic can validate collections too.

> Use standard Python `list` and `dict` types to validate arrays of items or dynamic key-value pairs.


### List

```python
class Student(BaseModel):
    name: str
    subjects: list[str]
```

Example:

```json
{
    "name": "Ravi",
    "subjects": [
        "Python",
        "FastAPI",
        "SQL"
    ]
}
```

### List of models

```python
class Product(BaseModel):
    name: str
    price: float

class Order(BaseModel):
    products: list[Product]
```

Example:

```json
{
    "products": [
        {
            "name": "Laptop",
            "price": 50000
        },
        {
            "name": "Mouse",
            "price": 1000
        }
    ]
}
```

### Dictionary

```python
class User(BaseModel):
    name: str
    settings: dict[str, str]
```

Example:

```json
{
    "name": "Ravi",
    "settings": {
        "theme": "dark",
        "language": "English"
    }
}
```

## 24. Custom Validation

Sometimes built-in validation is not enough.

We can create our own validation rule.

> When standard types and `Field` constraints aren't enough, you can write custom Python logic using the `@field_validator` decorator.

Example:

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if not value.isalpha():
            raise ValueError("Name must contain only letters")
        return value
```

Now:

```text
"Ravi"       → Valid
"Ravi123"    → Invalid
```

### Why custom validation?

For business rules such as:

```text
Age must be >= 18
Password must be strong
Quantity must be > 0
Start date must be before end date
```

## 25. Serialization / Deserialization

These two terms are important.

### Serialization

Converting a Python object into a format such as JSON.

> Converting incoming raw data (like a JSON string) into a structured Python object (Pydantic model).

```text
Python Object
      ↓
   JSON
```

Example:

```python
user.model_dump()
```

Result:

```python
{
    "name": "Ravi",
    "age": 30
}
```

### Deserialization

Converting incoming data into a Python/Pydantic object.

> Converting your Python Pydantic object back into a standard dictionary (`model.model_dump()`) or JSON string (`model.model_dump_json()`) so it can be sent over the network.

```text
JSON
 ↓
Pydantic Model
```

FastAPI and Pydantic handle much of this automatically.

### Simple idea

```text
Client
  ↓
JSON
  ↓
Pydantic Model
  ↓
Python Code
```

and back:

```text
Python Object
  ↓
Pydantic Model
  ↓
JSON
  ↓
Client
```

## 26. Response Models

A **response model** defines what the API should return.

> You can define the exact shape of the data your API will *return* by using the `response_model` parameter in your route decorator. This is useful for filtering out sensitive data (like passwords) before sending the response to the client.

Example:

```python
class UserResponse(BaseModel):
    id: int
    name: str
```

Use it in FastAPI:

```python
@app.get("/users/1", response_model=UserResponse)
def get_user():
    return {
        "id": 1,
        "name": "Ravi"
    }
```

The response follows the `UserResponse` structure.

### Why use response models?

They help to:

* Define the API response structure
* Validate returned data
* Prevent unwanted fields from being returned
* Generate better API documentation

---

## Key Takeaways

We should remember:

1. **Type hints** describe expected data types.
2. **Pydantic** validates application data.
3. **Request models** define incoming data.
4. **Field validation** defines rules for individual fields.
5. **Optional/default fields** allow missing values or provide defaults.
6. **Nested models** represent complex JSON structures.
7. **Lists/dictionaries** can also be validated.
8. **Custom validators** implement application-specific rules.
9. **Serialization** converts objects to data such as JSON.
10. **Deserialization** converts incoming data into Python/Pydantic objects.
11. **Response models** define the structure of API responses.

> **Pydantic defines what data we expect, validates it, and helps control what data we return.**


## 27. Relational vs NoSQL Databases

### Relational Database

Data is stored in **tables**.

> Stores data in strict tables with columns and rows (e.g., PostgreSQL, MySQL, SQLite). Best for structured data with clear relationships.

Examples:

* MySQL
* PostgreSQL
* SQL Server
* Oracle

Example:

```text
students
---------------------
id | name | age
---------------------
1  | Ravi | 21
2  | Arun | 22
```

Relational databases are useful when data has clear relationships.

---

### NoSQL Database

NoSQL databases commonly store data as **documents**.

> Stores data in flexible, JSON-like documents (e.g., MongoDB). Best for unstructured data or rapidly changing data models.

Example: MongoDB

```json
{
    "_id": 1,
    "name": "Ravi",
    "age": 21
}
```

### Simple comparison

```text
SQL
 ↓
Tables → Rows → Columns

MongoDB
 ↓
Collections → Documents
```

## 28. SQLAlchemy

**SQLAlchemy** is a Python library used to work with relational databases.

> The most popular Object-Relational Mapper (ORM) for Python. It translates Python classes and code into raw SQL queries behind the scenes, so you don't have to write SQL manually.

It provides tools to:

* Connect to databases
* Define models
* Execute queries
* Insert data
* Update data
* Delete data

Instead of writing database code everywhere, SQLAlchemy provides a consistent Python interface.

Example:

```python
from sqlalchemy import create_engine

engine = create_engine(
    "sqlite:///students.db"
)
```

---

## 29. Database Models

A database model represents a database table.

> Python classes that represent your database tables. While Pydantic models validate JSON data, SQLAlchemy models define the columns, data types, and primary keys of your actual database.

Example:

```python
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    age: Mapped[int]
```

This represents:

```text
students
----------------
id
name
age
```

### Simple idea

```text
Python Model
     ↓
Database Table
```

---

## 30. Sessions

A **database session** is used to communicate with the database.

> A session is a temporary workspace connected to your database. You add new objects or make changes to existing ones inside the session, and the database isn't actually updated until you specifically tell the session to `commit()`.

For example:

```text
FastAPI
   ↓
Session
   ↓
Database
```

A session can be used to:

* Read data
* Insert data
* Update data
* Delete data
* Commit changes

Example:

```python
student = Student(name="Ravi", age=21)

session.add(student)
session.commit()
```

### Simple idea

> **Session is the working connection/context used to perform database operations.**

---

## 31. CRUD with Database

Using a SQLAlchemy session to perform standard operations:

* **Create:** `session.add(new_user)` then `session.commit()`
* **Read:** `session.query(User).filter(User.id == 1).first()`
* **Update:** Modify the object (`user.name = "Bob"`), then `session.commit()`
* **Delete:** `session.delete(user)` then `session.commit()`


The same CRUD operations we learned earlier can now use a real database.

### Create

```python
student = Student(name="Ravi", age=21)

session.add(student)
session.commit()
```

### Read

```python
students = session.query(Student).all()
```

### Update

```python
student.name = "Arun"
session.commit()
```

### Delete

```python
session.delete(student)
session.commit()
```

So:

```text
POST   → INSERT
GET    → SELECT
PUT    → UPDATE
DELETE → DELETE
```

---

## 32. Relationships

> Connecting tables together (like a User having many Posts). SQLAlchemy uses a `relationship()` function to link models, allowing you to access related data seamlessly in Python (e.g., `user.posts` automatically fetches the user's posts).

Database tables often have relationships.

For example:

```text
Student
   ↓
Courses
```

One student can have many courses.

```text
Student
----------------
id
name

Course
----------------
id
name
student_id
```

This is a **one-to-many relationship**.

Other common relationships:

```text
One-to-One
One-to-Many
Many-to-Many
```

### Example

```text
Student 1
   ↓
   ├── Python
   ├── FastAPI
   └── SQL
```

SQLAlchemy can represent these relationships using `relationship()`.

---

## 33. Transactions

> A transaction groups multiple database steps into a single, all-or-nothing operation. If one step fails (e.g., deducting money succeeds but adding it to another account fails), you call `session.rollback()` to undo everything and prevent corrupted data.


A **transaction** is a group of database operations treated as one unit.

Example:

```text
Transfer ₹1000
     ↓
Remove ₹1000 from Account A
     ↓
Add ₹1000 to Account B
```

Both operations should succeed.

If something goes wrong:

```text
Rollback
```

Example:

```python
try:
    session.add(operation1)
    session.add(operation2)
    session.commit()
except:
    session.rollback()
```

### Simple idea

```text
All operations succeed
        ↓
      COMMIT

Something fails
        ↓
     ROLLBACK
```

---

## 34. Connection Pooling

Opening a database connection takes time.

Instead of creating a new connection for every request, applications can **reuse connections**.

A connection pool keeps several database connections ready.

> Opening a brand new connection to a database is slow. Connection pooling creates a batch of pre-opened connections. When FastAPI needs to talk to the database, it borrows a connection from the pool and returns it when finished, massively speeding up response times.

```text
             Connection Pool
          ┌────┬────┬────┬────┐
          │ C1 │ C2 │ C3 │ C4 │
          └────┴────┴────┴────┘
             ↑    ↑
           Requests
```

Request:

```text
Request
   ↓
Get connection from pool
   ↓
Execute query
   ↓
Return connection
```

### Why?

Connection pooling improves:

* Performance
* Resource usage
* Application scalability

---

## 35. Async Database Access

FastAPI supports asynchronous programming.

An asynchronous database library allows database operations to be performed without blocking the application in the same way as synchronous code.

> Traditional SQLAlchemy is synchronous (blocks the server while waiting for the database). For high-performance FastAPI apps, you use asynchronous drivers (like `asyncpg` for PostgreSQL) and `AsyncSession` so the server can handle other users while the database works.

Simple idea:

```text
Request
   ↓
Async database operation
   ↓
While waiting...
   ↓
Application can handle other work
```

Example concept:

```python
result = await session.execute(query)
```

For SQL databases, SQLAlchemy provides asynchronous support.

```text
FastAPI
   ↓
async endpoint
   ↓
Async SQLAlchemy
   ↓
Database
```

### Important

Using `async def` alone does **not** automatically make database operations asynchronous.

The database driver/library must also support async operations.

---

## 36. MongoDB Integration

**MongoDB** is a NoSQL document database.

Example document:

```json
{
    "name": "Ravi",
    "age": 21,
    "courses": [
        "Python",
        "FastAPI"
    ]
}
```

MongoDB structure:

```text
Database
   ↓
Collection
   ↓
Document
```

For example:

```text
college
   ↓
students
   ↓
{
    "name": "Ravi",
    "age": 21
}
```

FastAPI can work with MongoDB using Python MongoDB libraries such as **PyMongo** or its asynchronous APIs.

Simple flow:

```text
FastAPI
   ↓
MongoDB Driver
   ↓
MongoDB
```

> Because MongoDB is NoSQL, you don't use SQLAlchemy. Instead, you integrate it into FastAPI using **Motor** (an asynchronous Python driver for MongoDB) or **Beanie** (an Object Document Mapper that uses Pydantic to structure MongoDB documents).
---

### SQL Database Flow

```text
Client
  ↓
FastAPI Router
  ↓
Service
  ↓
Repository
  ↓
SQLAlchemy
  ↓
Session
  ↓
Database
```

Example:

```text
POST /students
       ↓
Student Schema
       ↓
Student Service
       ↓
Student Repository
       ↓
SQLAlchemy
       ↓
INSERT
       ↓
Database
```

---

### MongoDB Flow

```text
Client
  ↓
FastAPI
  ↓
Service
  ↓
Repository
  ↓
MongoDB Driver
  ↓
MongoDB
```

---

## Key Takeaways

We should remember:

1. **Relational database** → tables, rows and columns.
2. **NoSQL database** → commonly uses documents and collections.
3. **SQLAlchemy** → Python toolkit/ORM for relational databases.
4. **Database model** → represents a database table.
5. **Session** → used to perform database operations.
6. **CRUD** → Create, Read, Update and Delete database data.
7. **Relationships** → connect related tables/entities.
8. **Transactions** → group operations into one unit.
9. **Connection pooling** → reuses database connections.
10. **Async database access** → supports non-blocking database operations when using an async-compatible driver/library.
11. **MongoDB** → document-oriented NoSQL database.

> **FastAPI handles the request → Service handles the logic → Repository talks to the database → Database stores the data.**


## 37. `Depends()`

> > **Dependency Injection means giving a function the things it needs instead of making the function create them itself.**

FastAPI provides `Depends()` for Dependency Injection.

> The core tool in FastAPI used to inject shared logic, configuration, or data into your route endpoints. You declare it directly inside your function parameters.

Example:

```python
from fastapi import Depends, FastAPI

app = FastAPI()

def get_message():
    return "Hello"

@app.get("/")
def home(message=Depends(get_message)):
    return {"message": message}
```

Here:

```text
Depends(get_message)
        ↓
FastAPI calls get_message()
        ↓
Result is given to home()
```

We don't call:

```python
get_message()
```

ourselves.

FastAPI does it for us.

---

## 38. Dependency Functions

A **dependency function** is a normal Python function that provides something required by another function.

> Any regular Python function (or class) that returns a value can be a dependency. FastAPI runs this function *before* your route runs, and passes its return value directly into your endpoint as a variable.

Example:

```python
def get_current_user():
    return "Ravi"
```

Use it:

```python
@app.get("/profile")
def profile(user=Depends(get_current_user)):
    return {"user": user}
```

Flow:

```text
Request
   ↓
get_current_user()
   ↓
user
   ↓
profile()
```

A dependency can provide:

* Database session
* Current user
* Configuration
* Common parameters
* Permissions
* Other services

---

## 39. Nested Dependencies

A dependency can itself depend on another dependency.

> Dependencies can depend on other dependencies. FastAPI automatically resolves the entire chain of dependencies in the correct order before executing your final endpoint.

Example:

```python
def get_database():
    return "Database"

def get_user(db=Depends(get_database)):
    return "User from " + db

@app.get("/profile")
def profile(user=Depends(get_user)):
    return {"user": user}
```

Flow:

```text
profile()
   ↓
get_user()
   ↓
get_database()
```

So dependencies can form a chain.

```text
Route
  ↓
Dependency A
  ↓
Dependency B
  ↓
Dependency C
```

---

## 40. Database Dependencies

Database sessions are a very common use of dependency injection.

> The most common use case for Dependency Injection. A dependency function creates a database session, `yields` it to the route, and ensures it is safely closed after the request is finished.

Example:

```python
def get_db():
    db = create_session()

    try:
        yield db
    finally:
        db.close()
```

Use it:

```python
@app.get("/students")
def get_students(db=Depends(get_db)):
    return db.query(Student).all()
```

Flow:

```text
Request
   ↓
get_db()
   ↓
Database Session
   ↓
API function
   ↓
Database operation
   ↓
Session closed
```

### Why is this useful?

We don't need to create and close the database session in every API.

---

## 41. Authentication Dependencies

Authentication can also be implemented using dependencies.

Example:

```python
def get_current_user():
    # Check token
    # Find user
    return "Ravi"
```

Use it:

```python
@app.get("/profile")
def profile(user=Depends(get_current_user)):
    return {"user": user}
```

Now every protected API can reuse the same dependency.

```text
GET /profile
     ↓
Authentication dependency
     ↓
Check user
     ↓
API
```

If authentication fails, the dependency can raise an HTTP error.

---

## 42. Reusable Dependencies

The biggest advantage is **reuse**.

Suppose several APIs need the current user:

```python
@app.get("/profile")
def profile(user=Depends(get_current_user)):
    ...

@app.get("/orders")
def orders(user=Depends(get_current_user)):
    ...

@app.get("/payments")
def payments(user=Depends(get_current_user)):
    ...
```

We write the authentication logic once.

```text
get_current_user()
       ↓
 ┌─────┼─────┐
 ↓     ↓     ↓
Profile Orders Payments
```

This avoids duplicate code.

---

## 43. Dependency Overrides

During testing, we may want to replace a real dependency with a fake one.

For example, normally:

```python
def get_db():
    return production_database
```

During testing:

```python
def fake_db():
    return test_database
```

FastAPI allows us to override the dependency.

Conceptually:

```python
app.dependency_overrides[get_db] = fake_db
```

Now:

```text
Normal application
      ↓
get_db()
      ↓
Production DB
```

Testing:

```text
Test
 ↓
fake_db()
 ↓
Test DB
```

This is very useful for testing.

---

## 44. Dependency Testing

Dependencies make testing easier because we can replace real components.

For example, suppose an API depends on:

```text
Database
Authentication
External API
```

Testing can replace them with:

```text
Test Database
Fake User
Mock External API
```

Example:

```python
app.dependency_overrides[get_current_user] = fake_user
```

Then tests don't need real authentication.

### Simple idea

```text
Production
    ↓
Real dependency

Testing
    ↓
Fake dependency
```

---

### Simple Real-World Example

Imagine our Student API.

We need:

1. Database
2. Current user
3. Student API

```text
                 Student API
                     ↓
              Authentication
                     ↓
                Current User
                     ↓
                Database
                     ↓
              Student Records
```

FastAPI can manage these dependencies.

Example:

```python
def get_db():
    return database

def get_current_user():
    return "Ravi"

@app.get("/students")
def students(
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    return {
        "user": user,
        "students": db.get_students()
    }
```

The API function receives what it needs.

It doesn't create everything itself.

---

### Why Dependency Injection?

Without dependency injection:

```python
def get_students():
    db = create_database()
    user = authenticate()
    ...
```

The function creates everything itself.

With dependency injection:

```python
def get_students(
    db=Depends(get_db),
    user=Depends(get_current_user)
):
    ...
```

FastAPI provides the required objects.

### Benefits

* Less duplicate code
* Reusable components
* Easier testing
* Cleaner APIs
* Better separation of responsibilities

---

## Key Takeaways

We should remember:

1. **`Depends()`** → tells FastAPI that a function has a dependency.
2. **Dependency function** → provides something required by an API.
3. **Nested dependencies** → dependencies can depend on other dependencies.
4. **Database dependency** → commonly provides a database session.
5. **Authentication dependency** → commonly provides the current authenticated user.
6. **Reusable dependencies** → write common logic once and reuse it.
7. **Dependency overrides** → replace real dependencies during testing.
8. **Dependency testing** → makes APIs easier to test.

One-line mental model

> **The API says what it needs; FastAPI provides those dependencies.**

## 45. Authentication vs Authorization

### Authentication

Authentication verifies the **identity of a user**.

> Authentication asks "Who are you?"

> Verifying *who* you are (e.g., logging in with a username and password).

Example:

```text
Username + Password
        ↓
    Login
        ↓
    User verified
```

Question:

> **Who are you?**

---

### Authorization

Authorization checks what the authenticated user is **allowed to do**.

> Authorization asks "What are you allowed to do?"

> Verifying *what* you are allowed to do (e.g., checking if you have admin rights to delete a file).

Example:

```text
Admin → Can delete users
User  → Cannot delete users
```

Question:

> **What are you allowed to do?**

### Simple difference

```text
Authentication → Identity
Authorization  → Permission
```

---

## 46. Password Hashing

Passwords should **not be stored as plain text**.

> You should never store plain-text passwords in a database. Hashing (using libraries like `passlib` and `bcrypt`) converts a password into a scrambled, irreversible string of characters to keep it secure even if the database is hacked.

Bad:

```text
username: ravi
password: ravi123
```

Instead, store a **password hash**.

```text
Password
   ↓
Hashing algorithm
   ↓
Password hash
   ↓
Database
```

Example concept:

```text
"ravi123"
    ↓
"$2b$12$...."
```

During login:

```text
Entered Password
       ↓
Compare with stored hash
       ↓
Match?
```

FastAPI applications commonly use password-hashing libraries such as `pwdlib` with secure algorithms such as Argon2.

### Important

> **Hashing is not encryption.**

A password hash is designed to be one-way.

---

## 47. OAuth2

**OAuth2** is a standard/framework for **authorization**.

> A standard security protocol for handling authorization. FastAPI provides built-in tools (like `OAuth2PasswordBearer`) to easily set up a flow where a user submits their credentials and receives a token in return.

FastAPI provides tools for implementing OAuth2-based authentication flows.

A simple login flow:

```text
User
 ↓
Login
 ↓
Username + Password
 ↓
Authentication
 ↓
Access Token
 ↓
Client
```

Later:

```text
Client
 ↓
Access Token
 ↓
Protected API
```

### Important

OAuth2 is a framework for authorization flows. **JWT is a token format**, and they are not the same thing.

---

## 48. JWT

**JWT = JSON Web Token**

JWT is a commonly used format for carrying claims about a user.

> A secure, encoded string used to transmit information between the client and server. The server generates a JWT containing data (like the user's ID) and signs it with a secret key so it cannot be tampered with by the client.

A JWT contains information such as:

```text
User ID
Role
Expiration time
```

Conceptually:

```text
Header
.
Payload
.
Signature
```

Example payload:

```json
{
    "sub": "101",
    "role": "admin"
}
```

The server can verify the token's signature before trusting its claims.

### Simple flow

```text
Login
  ↓
Server creates JWT
  ↓
Client stores token
  ↓
Client sends token with requests
  ↓
Server verifies token
```

---

## 49. Access Tokens

An **access token** is used to access protected APIs.

> The short-lived JWT given to a user after a successful login. The client must include this token in the HTTP headers (e.g., `Authorization: Bearer <token>`) of future requests to prove they are authenticated.

Example request:

```text
GET /students
Authorization: Bearer <access-token>
```

Flow:

```text
Client
   ↓
Access Token
   ↓
FastAPI
   ↓
Verify Token
   ↓
Protected API
```

Access tokens are generally **short-lived**.

---

## 50. Refresh Tokens

When an access token expires, the user shouldn't necessarily have to log in again.

A **refresh token** can be used to obtain a new access token, depending on the authentication design.

> Because Access Tokens expire quickly (usually in 15-30 minutes for security), a longer-lived Refresh Token is used to silently request a *new* Access Token behind the scenes, so the user doesn't have to constantly type their password.

Simple flow:

```text
Login
  ↓
Access Token + Refresh Token
  ↓
Access Token expires
  ↓
Refresh Token
  ↓
New Access Token
```

### Simple difference

| Token         | Purpose                   |
| ------------- | ------------------------- |
| Access token  | Access APIs               |
| Refresh token | Obtain a new access token |

Refresh tokens require careful storage and security because they can be used to obtain new access tokens.

---

## 51. Role-Based Authorization

**Role-Based Access Control (RBAC)** gives permissions based on a user's role.

> Restricting access to endpoints based on a user's assigned group or role. For example, ensuring only users with the role `"admin"` can access the `/delete-database` endpoint.

Example:

```text
Admin
  ↓
Create
Read
Update
Delete

Student
  ↓
Read
```

User data:

```json
{
    "id": 101,
    "name": "Ravi",
    "role": "student"
}
```

Another user:

```json
{
    "id": 1,
    "name": "Admin",
    "role": "admin"
}
```

API:

```text
DELETE /users/101
```

The application checks:

```text
Is user authenticated?
        ↓
What is the user's role?
        ↓
Is that role allowed to delete?
```

---

## 52. Permission-Based Authorization

Instead of checking only roles, we can check **specific permissions**.

> A more detailed approach than roles. It restricts access based on specific, granular actions (e.g., `can_edit_post`, `can_view_billing`). A user might be allowed to edit their *own* profile but lack the permission to edit someone else's.

Example:

```text
Permissions:

student:read
student:create
student:update
student:delete
```

An admin might have:

```text
student:read
student:create
student:update
student:delete
```

A normal user might have:

```text
student:read
```

### Role vs Permission

```text
Role
 ↓
Admin

Permission
 ↓
student:delete
```

A role can have multiple permissions.

---

## 53. Protected Endpoints

A **protected endpoint** requires authentication before it can be accessed.

> API routes that require the user to be logged in. In FastAPI, you secure an endpoint by adding an authentication function into `Depends()`. If the user doesn't provide a valid token, FastAPI automatically blocks them with a `401 Unauthorized` error.

Example:

```python
@app.get("/profile")
def profile(
    user=Depends(get_current_user)
):
    return user
```

The dependency checks the user's authentication.

Flow:

```text
GET /profile
      ↓
Authentication dependency
      ↓
Token valid?
   ↙       ↘
 Yes        No
  ↓          ↓
Allow      401
```

For authorization:

```text
Token valid
     ↓
Check role/permission
     ↓
Allowed?
  ↙      ↘
Yes       No
 ↓         ↓
200       403
```

---

## 54. Complete Authentication Flow

A simple FastAPI application might work like this:

```text
              REGISTER
                 ↓
          Password Hashing
                 ↓
              Database
                 ↓
               LOGIN
                 ↓
       Username + Password
                 ↓
          Verify Password
                 ↓
      Access + Refresh Token
                 ↓
              CLIENT
                 ↓
       Authorization Header
                 ↓
          Protected API
                 ↓
       Verify Access Token
                 ↓
       Check Role/Permission
                 ↓
             Response
```

---

## 55. 401 vs 403

This is important.

### 401 Unauthorized

The client is **not properly authenticated**.

Examples:

```text
No token
Invalid token
Expired token
```

### 403 Forbidden

The user is authenticated but **does not have permission**.

Example:

```text
Logged-in student
       ↓
DELETE /users/10
       ↓
No delete permission
       ↓
403 Forbidden
```

Simple rule:

```text
401 → Authentication problem
403 → Authorization problem
```

---

## Key Takeaways

We should remember:

1. **Authentication** → Who are you?
2. **Authorization** → What can you do?
3. **Password hashing** → Never store plain-text passwords.
4. **OAuth2** → Standard framework for authorization flows.
5. **JWT** → A commonly used token format.
6. **Access token** → Used to access protected APIs.
7. **Refresh token** → Used to obtain a new access token.
8. **RBAC** → Authorization based on roles.
9. **Permissions** → Authorization based on specific actions.
10. **Protected endpoints** → APIs that require authentication/authorization.
11. **401** → Authentication problem.
12. **403** → Permission problem.

> **Login verifies the user → token represents the authenticated session/request → protected API verifies the token → authorization checks what the user can do.**
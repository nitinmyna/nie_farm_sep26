# MongoDB — Quick Reference Notes

## 1. MongoDB Components

**MongoDB Server (`mongod`)**
→ The actual database server that stores and manages MongoDB data.

**MongoDB Shell (`mongosh`)**
→ Command-line client used to connect to and interact with a MongoDB server.

```text
Application
    ↓
MongoDB Driver / mongosh
    ↓
MongoDB Server (mongod)
    ↓
Database → Collections → Documents
```

---

## 2. Install MongoDB Server on Windows

[Mongo DB Server Download - Community](https://www.mongodb.com/try/download/community) -> Community Server -> Select Package -> Version : 8.3.11 / Windows x64 / msi

ie `mongodb-windows-x86_64-8.3.11-signed.msi` From `https://www.mongodb.com`

Install **MongoDB Community Server**.

- MongoDB Server (mongod)	✅ Included
- MongoDB tools	✅ Included > mongodump, mongorestore, mongoexport, mongoimport, bsondump
- MongoDB Compass	✅ Optional during installation

After installation, verify:

```cmd
mongod --version
```

Expected:

```text
db version v8.x.x
```

Check MongoDB service:

```cmd
sc query MongoDB
```

If installed as a Windows service, start it with:

```cmd
net start MongoDB
```

Stop it with:

```cmd
net stop MongoDB
```

---

## 3. Install MongoDB Shell

Verify:

```cmd
mongosh --version
```

Example:

```text
2.8.2
```

> `mongosh` is only the **client/shell**. It does not contain the MongoDB database server.

---

# 4. Connect Using MongoDB Shell

Default local MongoDB connection:

```cmd
mongosh
```

Equivalent explicit connection:

```cmd
mongosh "mongodb://localhost:27017"
```

or:

```cmd
mongosh "mongodb://127.0.0.1:27017"
```

Typical prompt:

```text
test>
```

---

# 5. Basic `mongosh` Commands

[Mongo Shell Download](https://www.mongodb.com/try/download/shell) -> MongoDB Shell Download -> 2.12.0 / Windows x64 / zip | msi -> Download and Install


Show databases:

```javascript
show dbs
```

Select/create a database:

```javascript
use college
```

Show current database:

```javascript
db
```

Show collections:

```javascript
show collections
```

Create a collection:

```javascript
db.students.insertOne({
    name: "Ravi",
    age: 25,
    course: "Java"
})
```

Find documents:

```javascript
db.students.find()
```

Pretty output:

```javascript
db.students.find().pretty()
```

Find one:

```javascript
db.students.findOne()
```

---

# 6. Basic CRUD

### Create

```javascript
db.students.insertOne({
    name: "Ravi",
    age: 25
})
```

Multiple documents:

```javascript
db.students.insertMany([
    { name: "Ravi", age: 25 },
    { name: "Anu", age: 24 }
])
```

### Read

```javascript
db.students.find()
```

With condition:

```javascript
db.students.find({ age: 25 })
```

### Update

```javascript
db.students.updateOne(
    { name: "Ravi" },
    { $set: { age: 26 } }
)
```

### Delete

```javascript
db.students.deleteOne(
    { name: "Ravi" }
)
```

---

# 7. MongoDB Data Model

MongoDB is a **NoSQL document database**.

```text
MongoDB
  └── Database
       └── Collection
            └── Document
                 └── Field : Value
```

Example:

```javascript
{
    _id: ObjectId("..."),
    name: "Ravi",
    age: 25,
    skills: ["Java", "MongoDB"]
}
```

Think of it approximately as:

```text
Database   → Database
Collection → Table
Document   → Row
Field      → Column
```

But MongoDB documents are **flexible JSON-like/BSON documents**, so they don't have to follow a fixed relational-table structure.

---

# 8. Connect from Python

Install the official MongoDB Python driver:

```cmd
pip install pymongo
```

Python connection:

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["college"]

students = db["students"]
```

---

# 9. Python CRUD

### Insert

```python
students.insert_one({
    "name": "Ravi",
    "age": 25
})
```

### Find

```python
for student in students.find():
    print(student)
```

### Find One

```python
student = students.find_one({"name": "Ravi"})
print(student)
```

### Update

```python
students.update_one(
    {"name": "Ravi"},
    {"$set": {"age": 26}}
)
```

### Delete

```python
students.delete_one(
    {"name": "Ravi"}
)
```

---

# 10. Python Connection Flow

```text
Python Application
       ↓
PyMongo
       ↓
MongoClient
       ↓
mongodb://localhost:27017
       ↓
MongoDB Server (mongod)
       ↓
Database
       ↓
Collection
       ↓
Documents
```

### Important distinction

```text
mongod  → MongoDB SERVER
mongosh  → MongoDB SHELL / CLIENT
PyMongo  → Python DRIVER
```

**One-line memory aid:**

> **`mongod` stores the data, `mongosh` lets you interact with it manually, and PyMongo lets Python applications interact with it programmatically.**

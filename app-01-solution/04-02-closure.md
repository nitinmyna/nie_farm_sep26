## Student → Ticket transformation

The main transformation is:

| Student Application   | IT Service Desk      |
| --------------------- | -------------------- |
| `student_management`  | `it_service_desk`    |
| `students` collection | `tickets` collection |
| `StudentCreate`       | `TicketCreate`       |
| `StudentUpdate`       | `TicketUpdate`       |
| `StudentResponse`     | `TicketResponse`     |
| `student_helper()`    | `ticket_helper()`    |
| `/students`           | `/tickets`           |
| `student_id`          | `ticket_id`          |
| `Student not found`   | `Ticket not found`   |

### MongoDB structure

The application now looks like:

```text
FastAPI
   │
   ├── POST /tickets
   ├── GET /tickets
   ├── GET /tickets/{id}
   ├── PUT /tickets/{id}
   └── DELETE /tickets/{id}
          │
          ▼
      MongoClient
          │
          ▼
   MongoDB
      │
      └── it_service_desk
              │
              └── tickets
```

A MongoDB document will look approximately like:

```json
{
    "_id": "MongoDB ObjectId",
    "title": "Laptop not starting",
    "description": "Employee laptop does not power on",
    "category": "Hardware",
    "status": "NEW"
}
```

The API hides MongoDB's `_id` and exposes it as a string `id`:

```json
{
    "id": "68c...",
    "title": "Laptop not starting",
    "description": "Employee laptop does not power on",
    "category": "Hardware",
    "status": "NEW"
}
```

### Important learning point

Case 1 → **FastAPI basics**

```text
FastAPI
   ↓
GET /
```

Case 2 → **GET + in-memory data**

```text
FastAPI
   ↓
Dictionary
   ↓
GET
```

Case 3 → **Complete CRUD + Pydantic**

```text
FastAPI
   ↓
Pydantic
   ↓
CRUD
   ↓
Dictionary
```

Case 4 → **Real database**

```text
FastAPI
   ↓
Pydantic
   ↓
CRUD
   ↓
MongoDB
```

So **Case 4 should still remain a relatively simple Ticket CRUD application**. We should **not introduce User, authentication, assignment, comments, audit logs, etc. yet**. 

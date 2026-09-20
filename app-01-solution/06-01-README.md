# Case 6 — Final Enterprise IT Service Desk

Starting point:

| Phase | What we build                                          | Status             |
| ----- | ------------------------------------------------------ | ------------------ |
| **1** | Ticket CRUD + MongoDB                                  | ✅ Done             |
| **2** | Authentication + JWT + RBAC                            | ✅ Done             |
| **3** | Assignment + workflow + comments + attachments + audit | **🔨 Final — Now** |

The final `main.py` will contain the **complete application in one file**, so trainers and students can understand the whole progression without spending too much time on project structure.

## What we add in Case 6

### 1. Ticket assignment

A Team Lead/Admin can assign a ticket to a Support Engineer.

```text
Ticket
   ↓
Team Lead
   ↓
Assign
   ↓
Support Engineer
```

We add fields such as:

```text
created_by
assigned_to
```

---

### 2. Ticket workflow

We enforce the actual lifecycle:

```text
NEW
 ↓
ASSIGNED
 ↓
IN_PROGRESS
 ↓
RESOLVED
 ↓
CLOSED
```

and:

```text
IN_PROGRESS → ON_HOLD
ON_HOLD → IN_PROGRESS
```

Rather than allowing arbitrary status values, the API will validate the allowed workflow transitions.

---

### 3. Comments

Users can add comments to tickets.

```text
Ticket
   │
   ├── Comment
   ├── Comment
   └── Comment
```

Example:

```json
{
    "comment": "Checked the laptop. Hard disk appears to be failing."
}
```

---

### 4. Attachments

A ticket can contain supporting files.

```text
Ticket
   │
   ├── screenshot.png
   ├── error-log.txt
   └── invoice.pdf
```

FastAPI's `UploadFile` and `File` will be introduced here.

For a workshop application, we can store uploaded files locally and keep their metadata in MongoDB.

---

### 5. Audit Log

Important actions are recorded.

```text
AuditLog
   │
   ├── Ticket created
   ├── Ticket assigned
   ├── Status changed
   ├── Comment added
   ├── Attachment uploaded
   └── Ticket closed
```

Example:

```json
{
    "ticket_id": "...",
    "action": "STATUS_CHANGED",
    "performed_by": "engineer1",
    "old_value": "IN_PROGRESS",
    "new_value": "RESOLVED"
}
```

This gives students a very useful enterprise concept:

> **Who did what, to which ticket, and when?**

---

# Final entities

Our final MongoDB database becomes:

```text
it_service_desk
│
├── users
│
├── tickets
│
├── comments
│
├── attachments
│
└── audit_logs
```

The relationship is:

```text
                       ┌───────────┐
                       │   User    │
                       └─────┬─────┘
                             │
                    creates / assigned
                             │
                             ▼
                       ┌───────────┐
                       │  Ticket   │
                       └─────┬─────┘
                             │
               ┌─────────────┼─────────────┐
               ▼             ▼             ▼
          Comments      Attachments     AuditLogs
```

# Final API set

After Case 6, the students will have approximately:

### Authentication

```text
POST /users
POST /login
```

### Tickets

```text
POST   /tickets
GET    /tickets
GET    /tickets/{ticket_id}
PUT    /tickets/{ticket_id}
DELETE /tickets/{ticket_id}
```

### Assignment

```text
PUT /tickets/{ticket_id}/assign
```

### Workflow

```text
PUT /tickets/{ticket_id}/status
```

### Comments

```text
POST /tickets/{ticket_id}/comments
GET  /tickets/{ticket_id}/comments
```

### Attachments

```text
POST /tickets/{ticket_id}/attachments
GET  /tickets/{ticket_id}/attachments
```

### Audit

```text
GET /tickets/{ticket_id}/audit
```

---

# Final security model

The important part is that **Case 6 does not throw away Case 5 security**.

Every operation continues through:

```text
HTTP Request
     ↓
JWT Bearer Token
     ↓
get_current_user()
     ↓
require_roles()
     ↓
Business Rule
     ↓
MongoDB
```

For example:

```text
Employee
   │
   └── POST /tickets
             ↓
         JWT valid?
             ↓
          Role = 1?
             ↓
        Create ticket
```

Whereas:

```text
Employee
   │
   └── PUT /tickets/{id}/assign
             ↓
         JWT valid?
             ↓
       Role = 3 or 4?
             ↓
          Allowed
```

And:

```text
Employee
   │
   └── DELETE /tickets/{id}
             ↓
         JWT valid?
             ↓
          Role = 4?
             ↓
           403
```

---

# One important improvement over Case 5

Case 5 currently protects the endpoints with roles, but the final application should also implement **ownership/business authorization**.

For example, an Employee should not be able to do this:

```text
GET /tickets/{another_employee_ticket_id}
```

just because the Employee role is valid.

We therefore need two levels:

```text
Authentication
      ↓
"Who are you?"
      ↓
Authorization
      ↓
"What role do you have?"
      ↓
Business authorization
      ↓
"What are you allowed to do to THIS ticket?"
```

That makes the final application much closer to a real enterprise service desk.

---

## Final Case 6 learning outcome

By the end, the students will have built:

```text
FastAPI
   +
Pydantic
   +
MongoDB
   +
CRUD
   +
Password Hashing
   +
JWT
   +
OAuth2
   +
Swagger Authorization
   +
RBAC
   +
Ticket Assignment
   +
Workflow
   +
Comments
   +
File Upload
   +
Audit Logging
```

all in **one working application**.

That is a very good final capstone for a two-day FastAPI workshop because the students are not learning six unrelated applications—they are seeing **one reusable enterprise pattern applied to six different business domains**.



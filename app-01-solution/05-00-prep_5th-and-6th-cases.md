### 1. Ticket CRUD — ✅ Completed

```text
POST   /tickets
GET    /tickets
GET    /tickets/{id}
PUT    /tickets/{id}
DELETE /tickets/{id}

MongoDB
Pydantic validation
Exception handling
```

### 2. Authentication & Authorization — 🔐 Next

This is where we make the application **secured**.

```text
User
 │
 ├── Login
 │     ↓
 │   JWT Token
 │
 └── Access API
       ↓
   Bearer Token
```

Implement:

* User registration
* Password hashing
* Login
* JWT access token
* `OAuth2PasswordBearer`
* Protected endpoints
* Current logged-in user
* Role-Based Access Control (RBAC)

Roles:

```text
EMPLOYEE
SUPPORT_ENGINEER
TEAM_LEAD
ADMIN
```

Then enforce permissions:

```text
EMPLOYEE
  → Create ticket
  → View own tickets

SUPPORT_ENGINEER
  → View assigned tickets
  → Update assigned tickets

TEAM_LEAD
  → Assign/reassign tickets
  → Monitor team tickets

ADMIN
  → Manage users
  → Manage categories
  → Full access
```

### 3. Enterprise Service Desk Features — 🏢 Complete the application

After authentication is working, add the actual business workflow:

```text
Ticket
   │
   ├── Category
   ├── Created By → User
   ├── Assigned To → Support Engineer
   ├── Status
   ├── Comments
   ├── Attachments
   └── Audit Log
```

Ticket workflow:

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

IN_PROGRESS → ON_HOLD
ON_HOLD → IN_PROGRESS
```

And APIs such as:

```text
Assign ticket
Reassign ticket
Change status
Add comment
Upload attachment
View ticket history
```

### Final architecture

```text
                    ┌──────────────┐
                    │    User      │
                    └──────┬───────┘
                           │
                         Login
                           │
                           ▼
                    ┌──────────────┐
                    │     JWT      │
                    └──────┬───────┘
                           │
                    Bearer Token
                           │
                           ▼
┌─────────────────────────────────────────────────┐
│              FastAPI Application                 │
│                                                 │
│  Authentication → Authorization → Business     │
│                         Logic                   │
│                                                 │
│             Ticket CRUD + Workflow             │
└───────────────────────┬─────────────────────────┘
                        │
                        ▼
                  ┌───────────┐
                  │  MongoDB  │
                  └───────────┘
```



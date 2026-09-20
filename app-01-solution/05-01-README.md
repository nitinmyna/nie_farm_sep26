## Case 5 — Authentication + JWT + RBAC

For our IT Service Desk, let's define:

```text
1 → EMPLOYEE
2 → SUPPORT_ENGINEER
3 → TEAM_LEAD
4 → ADMIN
```

Your Student application currently has three roles and uses `require_roles()` to protect endpoints.  

For the **IT Service Desk**, I recommend adding the fourth role `ADMIN`.

### Security responsibilities

| Role             | Permissions                      |
| ---------------- | -------------------------------- |
| Employee         | Create ticket, view tickets      |
| Support Engineer | View/update assigned tickets     |
| Team Lead        | Assign/reassign, monitor tickets |
| Admin            | Full access + user management    |

### Authentication

```text
POST /users
      ↓
username + password + role
      ↓
password hashed
      ↓
MongoDB users collection
```

The password is **never stored as plain text**. Your existing implementation hashes the password before inserting the user document. 

### Login

```text
POST /login
      ↓
username + password
      ↓
verify hashed password
      ↓
create JWT
      ↓
access_token
```

Your existing `/login` implementation already follows this flow and returns:

```json
{
    "access_token": "...",
    "token_type": "bearer"
}
```



### JWT

For our application:

```json
{
    "sub": "employee1",
    "role": 1,
    "exp": "..."
}
```

The existing Student implementation puts `sub`, `role`, and `exp` into the JWT. 

### Swagger

This is particularly useful for your students.

```text
POST /login
      ↓
JWT token
      ↓
Swagger Authorize 🔒
      ↓
Bearer <token>
      ↓
Protected /tickets APIs
```

`OAuth2PasswordBearer(tokenUrl="/login")` is what connects the security dependency to the `/login` token endpoint. 

Then:

```python
current_user = Depends(get_current_user)
```

causes FastAPI to extract and validate the bearer token before executing the protected endpoint. 

---

# What we will actually change

We should **not rewrite everything from scratch**.

We will take your working Case 5 Student code and systematically transform:

```text
Student Management
        ↓
Enterprise IT Service Desk
```

### 1. Application

```text
Student Management API
        ↓
Enterprise IT Service Desk API
```

### 2. Database

```text
student_management
    ├── students
    └── users
```

becomes:

```text
it_service_desk
    ├── tickets
    └── users
```

### 3. Models

```text
StudentCreate
StudentUpdate
StudentResponse
```

remain from our Case 4 as:

```text
TicketCreate
TicketUpdate
TicketResponse
```

and we add:

```text
UserCreate
TokenResponse
```

### 4. Authentication

Keep:

```text
pwdlib
JWT
OAuth2PasswordBearer
OAuth2PasswordRequestForm
```


### 5. Authorization

Change:

```python
require_roles(1, 2, 3)
```

to the IT Service Desk roles.

For example:

```python
require_roles(1, 2, 3, 4)
```

for an API available to everyone.

And:

```python
require_roles(3, 4)
```

for Team Lead/Admin operations.

And:

```python
require_roles(4)
```

for Admin-only operations.

---

## Final Case 5 architecture

```text
                    ┌─────────────┐
                    │    User     │
                    └──────┬──────┘
                           │
                         LOGIN
                           │
                           ▼
                    ┌─────────────┐
                    │  Password   │
                    │  Verification│
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ JWT Token   │
                    │ sub + role  │
                    └──────┬──────┘
                           │
                    Bearer Token
                           │
                           ▼
                    ┌─────────────┐
                    │ FastAPI     │
                    │ Dependency  │
                    └──────┬──────┘
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
          Authentication       Authorization
          get_current_user()   require_roles()
                 │                   │
                 └─────────┬─────────┘
                           ▼
                  Protected /tickets
                           │
                           ▼
                       MongoDB
```

So **Case 5 is not just "add JWT"**. It teaches the students the complete security chain:

> **Authentication = Who are you?**
> **JWT = How do you prove it on subsequent requests?**
> **Authorization/RBAC = What are you allowed to do?**

Once **Authorize** is successful, Swagger automatically sends the Bearer token with subsequent protected requests. That behavior comes from the OAuth2 security scheme defined by `OAuth2PasswordBearer`. 

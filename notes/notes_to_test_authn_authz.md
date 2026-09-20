# User Creation 
### Admin Creation
```http
POST http://127.0.0.1:8000/users
```

```json
{
    "username": "admin",
    "password": "admin123",
    "role": 1
}
```

### Supervisor Creation

```http
POST http://127.0.0.1:8000/users
```

```json
{
    "username": "supervisor",
    "password": "super123",
    "role": 2
}
```

### Agent Creation

```http
POST http://127.0.0.1:8000/users
```

```json
{
    "username": "agent",
    "password": "agent123",
    "role": 3
}
```

MongoDB now contains:

```text
student_management
│
├── users
│   ├── admin
│   ├── supervisor
│   └── agent
│
└── students
```

Notice that MongoDB stores the **hashed password**, not:

```text
admin123
```

---

# Login — Admin

Thunder Client:

```http
POST http://127.0.0.1:8000/login
```

Body:

```json
{
    "username": "admin",
    "password": "admin123"
}
```

Response:

```json
{
    "access_token": "eyJhbGciOi...",
    "token_type": "bearer"
}
```

Copy the access token.

---

# Send JWT to Student API

In Thunder Client → **Auth** → **Bearer Token**.

Paste:

```text
eyJhbGciOi...
```

Or manually add:

```text
Authorization: Bearer eyJhbGciOi...
```

Now:

```http
GET /students
```

will work.

---

# Test Admin

Admin has all permissions.

```text
GET       /students          ✅
GET       /students/{id}     ✅
POST      /students          ✅
PUT       /students/{id}     ✅
DELETE    /students/{id}     ✅
```

---

# Test Supervisor

Login:

```http
POST /login
```

```json
{
    "username": "supervisor",
    "password": "super123"
}
```

Use the returned JWT.

Supervisor:

```text
GET       /students          ✅
GET       /students/{id}     ✅
POST      /students          ✅
PUT       /students/{id}     ✅
DELETE    /students/{id}     ❌
```

Delete should return:

```text
403 Forbidden
```

```json
{
    "detail": "Permission denied"
}
```

---

# Test Agent

Login:

```http
POST /login
```

```json
{
    "username": "agent",
    "password": "agent123"
}
```

Agent:

```text
GET       /students          ✅
GET       /students/{id}     ✅
POST      /students          ✅
PUT       /students/{id}     ❌
DELETE    /students/{id}     ❌
```

So:

```text
PUT    → 403
DELETE → 403
```

# Flow
```
/login
   ↓
username + password
   ↓
JWT access_token generated
   ↓
Swagger "Authorize" 🔒
   ↓
Swagger stores the token
   ↓
Protected resource
   ↓
Authorization: Bearer <JWT>
   ↓
OAuth2PasswordBearer extracts token
   ↓
get_current_user()
   ↓
JWT decoded + validated
   ↓
Role checked
   ↓
Resource executed
```
## Role mapping

This is the key change from your Student Management application:

```text
1 → EMPLOYEE
2 → SUPPORT_ENGINEER
3 → TEAM_LEAD
4 → ADMIN
```

Therefore:

```text
GET /tickets
GET /tickets/{id}
POST /tickets
        ↓
Employee / Engineer / Lead / Admin
```

while:

```text
PUT /tickets/{id}
        ↓
Support Engineer / Team Lead / Admin
```

and:

```text
DELETE /tickets/{id}
        ↓
Admin only
```

The authorization mechanism is the same pattern as your working Student Management code: `require_roles()` depends on `get_current_user()`, which validates the JWT before checking the user's role. 

### Swagger security flow

Run:

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Then:

```text
1. POST /users
       ↓
2. Create Employee / Engineer / Lead / Admin
       ↓
3. POST /login
       ↓
4. Get JWT
       ↓
5. Click Authorize 🔒
       ↓
6. Enter username/password
       ↓
7. Swagger obtains Bearer token
       ↓
8. Call /tickets
```

This follows the same OAuth2 password flow in your attached working application.  

**One important production note:** replace the hard-coded `SECRET_KEY` with an environment variable and use a strong randomly generated secret. For the workshop, keeping it in `main.py` makes the JWT concept easier to understand.

main.py It includes:

* Ticket CRUD
* MongoDB
* Password hashing
* JWT authentication
* OAuth2 / Swagger Authorize
* RBAC
* Ticket ownership
* Assignment/reassignment
* Status workflow
* Comments
* File attachments
* Audit logging

## Final Case 6 flow

The students now have one complete application:

```text
                         ┌─────────────┐
                         │    USER     │
                         └──────┬──────┘
                                │
                              LOGIN
                                │
                                ▼
                         ┌─────────────┐
                         │     JWT     │
                         └──────┬──────┘
                                │
                         Bearer Token
                                │
                                ▼
                       ┌────────────────┐
                       │   FastAPI      │
                       │ Authentication │
                       │ Authorization  │
                       └───────┬────────┘
                               │
                               ▼
                         ┌─────────────┐
                         │   TICKET    │
                         └──────┬──────┘
                                │
            ┌───────────────────┼───────────────────┐
            │                   │                   │
            ▼                   ▼                   ▼
       Assignment           Workflow            Comments
            │                   │                   │
            │                   │                   │
            └───────────────────┼───────────────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
              Attachments              Audit Logs
                    │                       │
                    └───────────┬───────────┘
                                ▼
                           ┌──────────┐
                           │ MongoDB  │
                           └──────────┘
```

### One deliberate teaching simplification

This is a **workshop-grade complete application**, not a production-ready service desk. In particular, file upload currently saves files to a local `uploads/` directory, and the JWT secret is in the source for simplicity. In production, you would move secrets to environment/secret management, validate file size/type, use proper object storage, add pagination, indexes, transactions where appropriate, and separate the application into routers/services/repositories.

This is a useful endpoint: we can start with the simple CRUD and progressively arrive at a complete enterprise-style application while preserving the same FastAPI concepts.

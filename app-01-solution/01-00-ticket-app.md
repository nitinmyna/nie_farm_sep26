# 1. `Enterprise IT Service Desk`

An organization has employees who raise IT service requests.

Example:

> Employee → raises laptop/access/network/software issue →
> Service Desk → assigns technician → technician works on it →
> resolves → employee confirms → ticket closed.

### Main actors

| Role             | Responsibilities                      |
| ---------------- | ------------------------------------- |
| Employee         | Create and view own tickets           |
| Support Engineer | View assigned tickets, update status  |
| Team Lead        | Assign/reassign tickets, monitor team |
| Admin            | Manage users/categories/configuration |

### Core entities

```text
User
Ticket
Category
Comment
Attachment
AuditLog
```

### Ticket lifecycle

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

with possible:

```text
IN_PROGRESS → ON_HOLD
ON_HOLD → IN_PROGRESS
```
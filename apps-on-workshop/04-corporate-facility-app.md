Corporate Facility Management

Employees raise:

* AC issue
* Electrical issue
* Housekeeping
* Meeting room
* Security
* IT

---

# 4. `Corporate Facility Management System`

An organization has employees who raise facility and workplace service requests.

Example:

> Employee → raises AC/electrical/housekeeping/meeting room/security/IT request →
> Facility Service Desk → assigns staff/vendor → staff works on it →
> resolves → employee confirms → request closed.

### Main actors

| Role             | Responsibilities                                            |
| ---------------- | ----------------------------------------------------------- |
| Employee         | Create and view own requests                                |
| Support Staff    | View assigned requests, work on them, update status         |
| Facility Manager | Assign/reassign requests, monitor support teams/vendors     |
| Admin            | Manage users, categories, locations, vendors, configuration |

### Core entities

```text
User

ServiceRequest

Category

Location

Comment

Attachment

AuditLog
```

### Request categories

```text
AC_ISSUE
ELECTRICAL_ISSUE
HOUSEKEEPING
MEETING_ROOM
SECURITY
IT
```

### Request lifecycle

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

### Example

```text
Employee
   ↓
Raises "AC Issue" request
   ↓
Facility Service Desk
   ↓
Assigns to HVAC Technician
   ↓
Technician checks and repairs AC
   ↓
RESOLVED
   ↓
Employee confirms
   ↓
CLOSED
```

### Additional example — Meeting Room

```text
Employee
   ↓
Raises "Meeting Room" request
   ↓
Facility Service Desk
   ↓
Assigns Facility Staff
   ↓
Room prepared / issue resolved
   ↓
RESOLVED
   ↓
Employee confirms
   ↓
CLOSED
```

This App 4 introduces an important enterprise concept beyond the earlier apps: **Location** — e.g., Building → Floor → Room — because facility requests are usually tied to a physical workplace location.

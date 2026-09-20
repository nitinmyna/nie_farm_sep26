# College Service Request System

Students/Faculty raise requests for:

* Bonafide certificate
* ID card
* Hostel
* Transport
* Library
* IT support

--- 

# 2. `College Service Request System`

A college has students and faculty who raise service requests for various college services.

Example:

> Student → raises Bonafide/ID Card/Hostel/Transport/Library/IT request →
> Service Office → assigns staff → staff processes it →
> resolves/completes → student/faculty receives the service → request closed.

### Main actors

| Role                    | Responsibilities                                   |
| ----------------------- | -------------------------------------------------- |
| Student                 | Create and view own requests                       |
| Faculty                 | Create and view own requests                       |
| Service Staff           | View assigned requests, process and update status  |
| Department/Service Lead | Assign/reassign requests, monitor service team     |
| Admin                   | Manage users, services, departments, configuration |

### Core entities

```text
User

ServiceRequest

ServiceCategory

Comment

Attachment

AuditLog
```

### Service categories

```text
BONAFIDE_CERTIFICATE
ID_CARD
HOSTEL
TRANSPORT
LIBRARY
IT_SUPPORT
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
Student
   ↓
Raises "Bonafide Certificate" request
   ↓
College Service Desk
   ↓
Assigns to Certificate Staff
   ↓
Staff processes request
   ↓
RESOLVED
   ↓
Student receives/confirms certificate
   ↓
CLOSED
```

This gives **App 2 the same service-request/ticketing architecture as App 1**, but with a **college-specific domain** and multiple service categories.

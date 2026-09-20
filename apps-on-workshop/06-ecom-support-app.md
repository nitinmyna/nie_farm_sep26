E-commerce Customer Support

Customer:

```text
Order problem
    ↓
Support ticket
    ↓
Agent
    ↓
Resolution
    ↓
Closure
```

---

# 6. `E-commerce Customer Support System`

An e-commerce platform has customers who raise support tickets for problems related to their orders.

Example:

> Customer → raises order-related support ticket → Customer Support Desk → assigns support agent → agent investigates and resolves the issue → customer confirms → ticket closed.

### Main actors

| Role              | Responsibilities                                         |
| ----------------- | -------------------------------------------------------- |
| Customer          | Create and view own support tickets                      |
| Support Agent     | View assigned tickets, investigate issues, update status |
| Support Team Lead | Assign/reassign tickets, monitor support team            |
| Admin             | Manage users, ticket categories, configuration           |

### Core entities

```text
User

Ticket

Category

Order

Comment

Attachment

AuditLog
```

### Ticket categories

```text
ORDER_NOT_RECEIVED
WRONG_ITEM
DAMAGED_ITEM
CANCEL_ORDER
REFUND
RETURN
PAYMENT_ISSUE
DELIVERY_ISSUE
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

### Example — Wrong Item

```text
Customer
   ↓
Raises "Wrong Item Received" ticket
   ↓
Customer Support Desk
   ↓
Assigns to Support Agent
   ↓
Agent verifies order details
   ↓
Coordinates return/replacement
   ↓
RESOLVED
   ↓
Customer confirms
   ↓
CLOSED
```

### Example — Refund

```text
Customer
   ↓
Raises "Refund" ticket
   ↓
Support Desk
   ↓
Assigns to Support Agent
   ↓
Agent verifies order/payment details
   ↓
Refund processed
   ↓
RESOLVED
   ↓
Customer confirms
   ↓
CLOSED
```

**App 6 introduces an important domain relationship:** `Ticket → Order`. A support ticket is associated with a specific customer order, allowing the support agent to investigate the problem using order, payment, delivery, return, and refund information.

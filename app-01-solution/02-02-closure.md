### Test in Swagger

**GET `/tickets`**

Response:

```json
[
    {
        "id": 1,
        "title": "Laptop not starting",
        "description": "Employee laptop does not power on",
        "category": "Hardware",
        "status": "NEW"
    },
    {
        "id": 2,
        "title": "VPN connection problem",
        "description": "Unable to connect to company VPN",
        "category": "Network",
        "status": "NEW"
    }
]
```

**GET `/tickets/1`**

Returns the first ticket.

**GET `/tickets/100`**

Returns:

```json
{
    "detail": "Ticket not found"
}
```

So the learning progression becomes:

```text
Enterprise IT Service Desk
       ↓
tickets dictionary
       ↓
GET /tickets
       ↓
GET /tickets/{id}
       ↓
HTTPException
```


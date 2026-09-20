from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# -----------------------------
# Pydantic Models
# -----------------------------

class TicketCreate(BaseModel):
    title: str
    description: str
    category: str
    status: str


class Ticket(TicketCreate):
    id: int


class TicketUpdate(BaseModel):
    title: str
    description: str
    category: str
    status: str


# -----------------------------
# Temporary Database
# -----------------------------

tickets = {
    # Think of 'tickets' as our temporary database.
    # The key is the ticket ID.

    1: {
        "id": 1,
        "title": "Laptop not starting",
        "description": "Employee laptop does not power on",
        "category": "Hardware",
        "status": "NEW"
    },

    2: {
        "id": 2,
        "title": "VPN connection problem",
        "description": "Unable to connect to company VPN",
        "category": "Network",
        "status": "NEW"
    }
}


# -----------------------------
# GET /
# -----------------------------

@app.get("/")
def home():
    return {"message": "Enterprise IT Service Desk API"}


# -----------------------------
# GET /tickets
# -----------------------------

@app.get("/tickets", response_model=list[Ticket])
def get_tickets():
    return list(tickets.values())


# -----------------------------
# GET /tickets/{ticket_id}
# -----------------------------

@app.get("/tickets/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int):

    if ticket_id not in tickets:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return tickets[ticket_id]


# -----------------------------
# POST /tickets
# -----------------------------

@app.post(
    "/tickets",
    response_model=Ticket,
    status_code=201
)
def create_ticket(ticket: TicketCreate):

    new_id = max(tickets.keys(), default=0) + 1

    new_ticket = {
        "id": new_id,
        **ticket.model_dump()
    }

    tickets[new_id] = new_ticket

    return new_ticket


# -----------------------------
# PUT /tickets/{ticket_id}
# -----------------------------

@app.put(
    "/tickets/{ticket_id}",
    response_model=Ticket
)
def update_ticket(
    ticket_id: int,
    ticket: TicketUpdate
):

    if ticket_id not in tickets:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    tickets[ticket_id] = {
        "id": ticket_id,
        **ticket.model_dump()
    }

    return tickets[ticket_id]


# -----------------------------
# DELETE /tickets/{ticket_id}
# -----------------------------

@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int):

    if ticket_id not in tickets:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    del tickets[ticket_id]

    return {
        "message": "Ticket deleted successfully"
    }
from fastapi import FastAPI, HTTPException

app = FastAPI()

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


# GET /
@app.get("/")
def home():
    return {"message": "Enterprise IT Service Desk API"}


# GET /tickets
@app.get("/tickets")
def get_tickets():
    return list(tickets.values())


# GET /tickets/1
# GET /tickets/100 → {"detail": "Ticket not found"}
@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):

    if ticket_id not in tickets:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return tickets[ticket_id]
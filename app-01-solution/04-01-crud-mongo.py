from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from pymongo import MongoClient
from bson import ObjectId
from typing import Optional


# ---------------------------------------------------------
# 1. FastAPI Application
# ---------------------------------------------------------

app = FastAPI(
    title="Enterprise IT Service Desk API",
    description="IT Service Desk REST API using FastAPI and MongoDB",
    version="2.0.0"
)


# ---------------------------------------------------------
# 2. MongoDB Connection
# ---------------------------------------------------------

MONGO_URL = "mongodb://localhost:27017"

client = MongoClient(MONGO_URL)

db = client["it_service_desk"]

tickets_collection = db["tickets"]


# ---------------------------------------------------------
# 3. Pydantic Models
# ---------------------------------------------------------

class TicketCreate(BaseModel):

    title: str = Field(
        min_length=5,
        max_length=100
    )

    description: str = Field(
        min_length=10,
        max_length=500
    )

    category: str = Field(
        min_length=2,
        max_length=50
    )

    status: str = Field(
        min_length=2,
        max_length=30
    )


class TicketUpdate(BaseModel):

    title: Optional[str] = Field(
        default=None,
        min_length=5,
        max_length=100
    )

    description: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=500
    )

    category: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50
    )

    status: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=30
    )


class TicketResponse(BaseModel):

    id: str
    title: str
    description: str
    category: str
    status: str


# ---------------------------------------------------------
# 4. Helper Function
# ---------------------------------------------------------

def ticket_helper(ticket) -> dict:
    """
    Convert MongoDB document into API response format.
    """

    return {
        "id": str(ticket["_id"]),
        "title": ticket["title"],
        "description": ticket["description"],
        "category": ticket["category"],
        "status": ticket["status"]
    }


# ---------------------------------------------------------
# 5. Home API
# ---------------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Enterprise IT Service Desk API",
        "version": "2.0.0"
    }


# ---------------------------------------------------------
# 6. CREATE Ticket
# ---------------------------------------------------------

@app.post(
    "/tickets",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED
)
def create_ticket(ticket: TicketCreate):

    ticket_data = ticket.model_dump()

    result = tickets_collection.insert_one(ticket_data)

    created_ticket = tickets_collection.find_one(
        {"_id": result.inserted_id}
    )

    return ticket_helper(created_ticket)


# ---------------------------------------------------------
# 7. GET All Tickets
# ---------------------------------------------------------

@app.get(
    "/tickets",
    response_model=list[TicketResponse]
)
def get_tickets():

    tickets = tickets_collection.find()

    return [
        ticket_helper(ticket)
        for ticket in tickets
    ]


# ---------------------------------------------------------
# 8. GET Ticket by ID
# ---------------------------------------------------------

@app.get(
    "/tickets/{ticket_id}",
    response_model=TicketResponse
)
def get_ticket(ticket_id: str):

    # Validate MongoDB ObjectId

    if not ObjectId.is_valid(ticket_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket ID"
        )

    ticket = tickets_collection.find_one(
        {"_id": ObjectId(ticket_id)}
    )

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    return ticket_helper(ticket)


# ---------------------------------------------------------
# 9. UPDATE Ticket
# ---------------------------------------------------------

@app.put(
    "/tickets/{ticket_id}",
    response_model=TicketResponse
)
def update_ticket(
    ticket_id: str,
    ticket: TicketUpdate
):

    if not ObjectId.is_valid(ticket_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket ID"
        )

    update_data = ticket.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )

    result = tickets_collection.update_one(
        {"_id": ObjectId(ticket_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    updated_ticket = tickets_collection.find_one(
        {"_id": ObjectId(ticket_id)}
    )

    return ticket_helper(updated_ticket)


# ---------------------------------------------------------
# 10. DELETE Ticket
# ---------------------------------------------------------

@app.delete(
    "/tickets/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_ticket(ticket_id: str):

    if not ObjectId.is_valid(ticket_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket ID"
        )

    result = tickets_collection.delete_one(
        {"_id": ObjectId(ticket_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    return None
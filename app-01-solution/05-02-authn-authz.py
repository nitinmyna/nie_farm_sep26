from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from pymongo import MongoClient
from bson import ObjectId
from pwdlib import PasswordHash
from typing import Optional
import jwt
from datetime import datetime, timedelta, timezone


# =========================================================
# 1. FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Enterprise IT Service Desk API",
    description="FastAPI + MongoDB + JWT Authentication + RBAC",
    version="3.0.0"
)


# =========================================================
# 2. MONGODB
# =========================================================

MONGO_URL = "mongodb://localhost:27017"

client = MongoClient(MONGO_URL)

db = client["it_service_desk"]

tickets_collection = db["tickets"]
users_collection = db["users"]


# =========================================================
# 3. PASSWORD HASHING
# =========================================================

password_hash = PasswordHash.recommended()


# =========================================================
# 4. JWT CONFIGURATION
# =========================================================

SECRET_KEY = "ITServiceDeskSecurityKey-ChangeThis"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# =========================================================
# 5. OAUTH2
# =========================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)


# =========================================================
# 6. PYDANTIC MODELS
# =========================================================


# -----------------------------
# Ticket Models
# -----------------------------

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


# -----------------------------
# User Models
# -----------------------------

class UserCreate(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=30
    )

    password: str = Field(
        min_length=6
    )

    # 1 = Employee
    # 2 = Support Engineer
    # 3 = Team Lead
    # 4 = Admin

    role: int = Field(
        ge=1,
        le=4
    )


class TokenResponse(BaseModel):

    access_token: str
    token_type: str


# =========================================================
# 7. HELPER FUNCTIONS
# =========================================================


def ticket_helper(ticket) -> dict:
    """
    Convert MongoDB ticket document
    into API response format.
    """

    return {
        "id": str(ticket["_id"]),
        "title": ticket["title"],
        "description": ticket["description"],
        "category": ticket["category"],
        "status": ticket["status"]
    }


def user_helper(user) -> dict:
    """
    Convert MongoDB user document
    into API response format.

    Password is deliberately not returned.
    """

    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "role": user["role"]
    }


# =========================================================
# 8. CREATE JWT
# =========================================================


def create_access_token(
    username: str,
    role: int
):

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "role": role,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


# =========================================================
# 9. GET CURRENT USER
# =========================================================


def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")
        role = payload.get("role")

        if username is None or role is None:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = users_collection.find_one(
        {"username": username}
    )

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


# =========================================================
# 10. ROLE AUTHORIZATION
# =========================================================


def require_roles(*allowed_roles):

    def role_checker(
        current_user=Depends(get_current_user)
    ):

        if current_user["role"] not in allowed_roles:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )

        return current_user

    return role_checker


# =========================================================
# 11. HOME
# =========================================================


@app.get("/")
def home():

    return {
        "message": "Enterprise IT Service Desk API",
        "version": "3.0.0"
    }


# =========================================================
# 12. CREATE USER
# =========================================================

# Workshop/demo setup.
#
# In a production application, user creation should
# normally be protected by an appropriate authorization
# policy.


@app.post("/users")
def create_user(user: UserCreate):

    existing_user = users_collection.find_one(
        {"username": user.username}
    )

    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    hashed_password = password_hash.hash(
        user.password
    )

    user_data = {
        "username": user.username,
        "password": hashed_password,
        "role": user.role
    }

    result = users_collection.insert_one(
        user_data
    )

    created_user = users_collection.find_one(
        {"_id": result.inserted_id}
    )

    return user_helper(created_user)


# =========================================================
# 13. LOGIN
# =========================================================


@app.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = users_collection.find_one(
        {"username": form_data.username}
    )

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not password_hash.verify(
        form_data.password,
        user["password"]
    ):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token(
        user["username"],
        user["role"]
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =========================================================
# 14. GET ALL TICKETS
# =========================================================

@app.get(
    "/tickets",
    response_model=list[TicketResponse]
)
def get_tickets(
    current_user=Depends(
        require_roles(1, 2, 3, 4)
    )
):

    tickets = tickets_collection.find()

    return [
        ticket_helper(ticket)
        for ticket in tickets
    ]


# =========================================================
# 15. GET ONE TICKET
# =========================================================

@app.get(
    "/tickets/{ticket_id}",
    response_model=TicketResponse
)
def get_ticket(
    ticket_id: str,
    current_user=Depends(
        require_roles(1, 2, 3, 4)
    )
):

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


# =========================================================
# 16. CREATE TICKET
# =========================================================

@app.post(
    "/tickets",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED
)
def create_ticket(
    ticket: TicketCreate,
    current_user=Depends(
        require_roles(1, 2, 3, 4)
    )
):

    ticket_data = ticket.model_dump()

    result = tickets_collection.insert_one(
        ticket_data
    )

    created_ticket = tickets_collection.find_one(
        {"_id": result.inserted_id}
    )

    return ticket_helper(created_ticket)


# =========================================================
# 17. UPDATE TICKET
# =========================================================

@app.put(
    "/tickets/{ticket_id}",
    response_model=TicketResponse
)
def update_ticket(
    ticket_id: str,
    ticket: TicketUpdate,
    current_user=Depends(
        require_roles(2, 3, 4)
    )
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


# =========================================================
# 18. DELETE TICKET
# =========================================================

@app.delete(
    "/tickets/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_ticket(
    ticket_id: str,
    current_user=Depends(
        require_roles(4)
    )
):

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
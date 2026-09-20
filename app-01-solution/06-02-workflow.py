

from fastapi import (
    FastAPI,
    HTTPException,
    status,
    Depends,
    UploadFile,
    File
)

from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm
)

from pydantic import BaseModel, Field

from pymongo import MongoClient

from bson import ObjectId

from pwdlib import PasswordHash

from typing import Optional

import jwt

from datetime import datetime, timedelta, timezone

import os
import shutil
import uuid


# =========================================================
# 1. FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="Enterprise IT Service Desk API",
    description=(
        "Complete IT Service Desk API using "
        "FastAPI + MongoDB + JWT Authentication + RBAC"
    ),
    version="4.0.0"
)


# =========================================================
# 2. MONGODB
# =========================================================

MONGO_URL = "mongodb://localhost:27017"

client = MongoClient(MONGO_URL)

db = client["it_service_desk"]

users_collection = db["users"]

tickets_collection = db["tickets"]

comments_collection = db["comments"]

attachments_collection = db["attachments"]

audit_logs_collection = db["audit_logs"]


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
# 6. ROLES
# =========================================================

EMPLOYEE = 1

SUPPORT_ENGINEER = 2

TEAM_LEAD = 3

ADMIN = 4


# =========================================================
# 7. TICKET STATUS
# =========================================================

NEW = "NEW"

ASSIGNED = "ASSIGNED"

IN_PROGRESS = "IN_PROGRESS"

ON_HOLD = "ON_HOLD"

RESOLVED = "RESOLVED"

CLOSED = "CLOSED"


ALLOWED_STATUSES = {
    NEW,
    ASSIGNED,
    IN_PROGRESS,
    ON_HOLD,
    RESOLVED,
    CLOSED
}


# =========================================================
# 8. UPLOAD DIRECTORY
# =========================================================

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)


# =========================================================
# 9. PYDANTIC MODELS
# =========================================================


# ---------------------------------------------------------
# Ticket Models
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


class TicketResponse(BaseModel):

    id: str

    title: str

    description: str

    category: str

    status: str

    created_by: str

    assigned_to: Optional[str] = None


# ---------------------------------------------------------
# User Models
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Assignment Model
# ---------------------------------------------------------

class TicketAssignment(BaseModel):

    assigned_to: str


# ---------------------------------------------------------
# Status Model
# ---------------------------------------------------------

class TicketStatusUpdate(BaseModel):

    status: str


# ---------------------------------------------------------
# Comment Model
# ---------------------------------------------------------

class CommentCreate(BaseModel):

    comment: str = Field(
        min_length=1,
        max_length=1000
    )


class CommentResponse(BaseModel):

    id: str

    ticket_id: str

    comment: str

    created_by: str

    created_at: str


# =========================================================
# 10. HELPER FUNCTIONS
# =========================================================


def user_helper(user) -> dict:

    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "role": user["role"]
    }


def ticket_helper(ticket) -> dict:

    return {
        "id": str(ticket["_id"]),
        "title": ticket["title"],
        "description": ticket["description"],
        "category": ticket["category"],
        "status": ticket["status"],
        "created_by": ticket["created_by"],
        "assigned_to": ticket.get("assigned_to")
    }


def comment_helper(comment) -> dict:

    return {
        "id": str(comment["_id"]),
        "ticket_id": str(comment["ticket_id"]),
        "comment": comment["comment"],
        "created_by": comment["created_by"],
        "created_at": comment["created_at"]
    }


# =========================================================
# 11. AUDIT LOG
# =========================================================


def create_audit_log(
    ticket_id,
    action,
    performed_by,
    details=""
):

    audit_logs_collection.insert_one(
        {
            "ticket_id": ObjectId(ticket_id),
            "action": action,
            "performed_by": performed_by,
            "details": details,
            "created_at": datetime.now(
                timezone.utc
            ).isoformat()
        }
    )


# =========================================================
# 12. CREATE JWT
# =========================================================


def create_access_token(
    username: str,
    role: int
):

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
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
# 13. GET CURRENT USER
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
# 14. ROLE AUTHORIZATION
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
# 15. TICKET ACCESS / OWNERSHIP
# =========================================================


def can_access_ticket(
    ticket,
    current_user
):

    role = current_user["role"]

    username = current_user["username"]

    # Admin and Team Lead can access all tickets

    if role in [ADMIN, TEAM_LEAD]:

        return True

    # Support Engineer can access
    # tickets assigned to them

    if role == SUPPORT_ENGINEER:

        return ticket.get(
            "assigned_to"
        ) == username

    # Employee can access
    # tickets created by themselves

    if role == EMPLOYEE:

        return ticket.get(
            "created_by"
        ) == username

    return False


# =========================================================
# 16. HOME
# =========================================================


@app.get("/")
def home():

    return {
        "message": "Enterprise IT Service Desk API",
        "version": "4.0.0"
    }


# =========================================================
# 17. CREATE USER
# =========================================================


@app.post("/users")
def create_user(
    user: UserCreate
):

    existing_user = users_collection.find_one(
        {
            "username": user.username
        }
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
        {
            "_id": result.inserted_id
        }
    )

    return user_helper(
        created_user
    )


# =========================================================
# 18. LOGIN
# =========================================================


@app.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = users_collection.find_one(
        {
            "username": form_data.username
        }
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
# 19. CREATE TICKET
# =========================================================


@app.post(
    "/tickets",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED
)
def create_ticket(
    ticket: TicketCreate,
    current_user=Depends(
        require_roles(
            EMPLOYEE,
            SUPPORT_ENGINEER,
            TEAM_LEAD,
            ADMIN
        )
    )
):

    ticket_data = ticket.model_dump()

    ticket_data["status"] = NEW

    ticket_data["created_by"] = (
        current_user["username"]
    )

    ticket_data["assigned_to"] = None

    result = tickets_collection.insert_one(
        ticket_data
    )

    created_ticket = tickets_collection.find_one(
        {
            "_id": result.inserted_id
        }
    )

    create_audit_log(
        str(result.inserted_id),
        "TICKET_CREATED",
        current_user["username"]
    )

    return ticket_helper(
        created_ticket
    )


# =========================================================
# 20. GET ALL TICKETS
# =========================================================


@app.get(
    "/tickets",
    response_model=list[TicketResponse]
)
def get_tickets(
    current_user=Depends(
        get_current_user
    )
):

    role = current_user["role"]

    username = current_user["username"]

    # Admin / Team Lead → all tickets

    if role in [ADMIN, TEAM_LEAD]:

        tickets = tickets_collection.find()

    # Support Engineer → assigned tickets

    elif role == SUPPORT_ENGINEER:

        tickets = tickets_collection.find(
            {
                "assigned_to": username
            }
        )

    # Employee → own tickets

    else:

        tickets = tickets_collection.find(
            {
                "created_by": username
            }
        )

    return [
        ticket_helper(ticket)
        for ticket in tickets
    ]


# =========================================================
# 21. GET ONE TICKET
# =========================================================


@app.get(
    "/tickets/{ticket_id}",
    response_model=TicketResponse
)
def get_ticket(
    ticket_id: str,
    current_user=Depends(
        get_current_user
    )
):

    if not ObjectId.is_valid(ticket_id):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket ID"
        )

    ticket = tickets_collection.find_one(
        {
            "_id": ObjectId(ticket_id)
        }
    )

    if ticket is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    if not can_access_ticket(
        ticket,
        current_user
    ):

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot access this ticket"
        )

    return ticket_helper(
        ticket
    )


# =========================================================
# 22. UPDATE TICKET
# =========================================================


@app.put(
    "/tickets/{ticket_id}",
    response_model=TicketResponse
)
def update_ticket(
    ticket_id: str,
    ticket: TicketUpdate,
    current_user=Depends(
        require_roles(
            EMPLOYEE,
            SUPPORT_ENGINEER,
            TEAM_LEAD,
            ADMIN
        )
    )
):

    if not ObjectId.is_valid(ticket_id):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket ID"
        )

    existing_ticket = tickets_collection.find_one(
        {
            "_id": ObjectId(ticket_id)
        }
    )

    if existing_ticket is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    if not can_access_ticket(
        existing_ticket,
        current_user
    ):

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot update this ticket"
        )

    update_data = ticket.model_dump(
        exclude_unset=True
    )

    if not update_data:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )

    tickets_collection.update_one(
        {
            "_id": ObjectId(ticket_id)
        },
        {
            "$set": update_data
        }
    )

    updated_ticket = tickets_collection.find_one(
        {
            "_id": ObjectId(ticket_id)
        }
    )

    create_audit_log(
        ticket_id,
        "TICKET_UPDATED",
        current_user["username"]
    )

    return ticket_helper(
        updated_ticket
    )


# =========================================================
# 23. DELETE TICKET
# =========================================================


@app.delete(
    "/tickets/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_ticket(
    ticket_id: str,
    current_user=Depends(
        require_roles(ADMIN)
    )
):

    if not ObjectId.is_valid(ticket_id):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket ID"
        )

    result = tickets_collection.delete_one(
        {
            "_id": ObjectId(ticket_id)
        }
    )

    if result.deleted_count == 0:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    create_audit_log(
        ticket_id,
        "TICKET_DELETED",
        current_user["username"]
    )

    return None


# =========================================================
# 24. ASSIGN / REASSIGN TICKET
# =========================================================


@app.put(
    "/tickets/{ticket_id}/assign",
    response_model=TicketResponse
)
def assign_ticket(
    ticket_id: str,
    assignment: TicketAssignment,
    current_user=Depends(
        require_roles(
            TEAM_LEAD,
            ADMIN
        )
    )
):

    if not ObjectId.is_valid(ticket_id):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket ID"
        )

    ticket = tickets_collection.find_one(
        {
            "_id": ObjectId(ticket_id)
        }
    )

    if ticket is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    engineer = users_collection.find_one(
        {
            "username": assignment.assigned_to,
            "role": SUPPORT_ENGINEER
        }
    )

    if engineer is None:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Support Engineer not found"
        )

    old_assignee = ticket.get(
        "assigned_to"
    )

    tickets_collection.update_one(
        {
            "_id": ObjectId(ticket_id)
        },
        {
            "$set": {
                "assigned_to":
                    assignment.assigned_to,
                "status": ASSIGNED
            }
        }
    )

    create_audit_log(
        ticket_id,
        "TICKET_ASSIGNED",
        current_user["username"],
        f"Assigned to {assignment.assigned_to}"
    )

    if old_assignee:

        create_audit_log(
            ticket_id,
            "TICKET_REASSIGNED",
            current_user["username"],
            f"Changed from {old_assignee} "
            f"to {assignment.assigned_to}"
        )

    updated_ticket = tickets_collection.find_one(
        {
            "_id": ObjectId(ticket_id)
        }
    )

    return ticket_helper(
        updated_ticket
    )


# =========================================================
# 25. CHANGE TICKET STATUS
# =========================================================


@app.put(
    "/tickets/{ticket_id}/status",
    response_model=TicketResponse
)
def update_ticket_status(
    ticket_id: str,
    status_update: TicketStatusUpdate,
    current_user=Depends(
        get_current_user
    )
):

    if not ObjectId.is_valid(ticket_id):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket ID"
        )

    new_status = status_update.status.upper()

    if new_status not in ALLOWED_STATUSES:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket status"
        )

    ticket = tickets_collection.find_one(
        {
            "_id": ObjectId(ticket_id)
        }
    )

    if ticket is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    if not can_access_ticket(
        ticket,
        current_user
    ):

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot update this ticket"
        )

    old_status = ticket["status"]

    # ---------------------------------------------
    # Allowed workflow transitions
    # ---------------------------------------------

    valid_transitions = {

        NEW: [ASSIGNED],

        ASSIGNED: [IN_PROGRESS],

        IN_PROGRESS: [
            ON_HOLD,
            RESOLVED
        ],

        ON_HOLD: [
            IN_PROGRESS
        ],

        RESOLVED: [
            CLOSED
        ],

        CLOSED: []
    }

    if new_status not in valid_transitions[
        old_status
    ]:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Cannot change status "
                f"from {old_status} "
                f"to {new_status}"
            )
        )

    tickets_collection.update_one(
        {
            "_id": ObjectId(ticket_id)
        },
        {
            "$set": {
                "status": new_status
            }
        }
    )

    create_audit_log(
        ticket_id,
        "STATUS_CHANGED",
        current_user["username"],
        f"{old_status} -> {new_status}"
    )

    updated_ticket = tickets_collection.find_one(
        {
            "_id": ObjectId(ticket_id)
        }
    )

    return ticket_helper(
        updated_ticket
    )


# =========================================================
# 26. ADD COMMENT
# =========================================================


@app.post(
    "/tickets/{ticket_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED
)
def add_comment(
    ticket_id: str,
    comment: CommentCreate,
    current_user=Depends(
        get_current_user
    )
):

    if not ObjectId.is_valid(ticket_id):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket ID"
        )

    ticket = tickets_collection.find_one(
        {
            "_id": ObjectId(ticket_id)
        }
    )

    if ticket is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    if not can_access_ticket(
        ticket,
        current_user
    ):

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot comment on this ticket"
        )

    comment_data = {

        "ticket_id": ObjectId(ticket_id),

        "comment": comment.comment,

        "created_by": current_user["username"],

        "created_at": datetime.now(
            timezone.utc
        ).isoformat()
    }

    result = comments_collection.insert_one(
        comment_data
    )

    created_comment = comments_collection.find_one(
        {
            "_id": result.inserted_id
        }
    )

    create_audit_log(
        ticket_id,
        "COMMENT_ADDED",
        current_user["username"]
    )

    return comment_helper(
        created_comment
    )


# =========================================================
# 27. GET COMMENTS
# =========================================================


@app.get(
    "/tickets/{ticket_id}/comments",
    response_model=list[CommentResponse]
)
def get_comments(
    ticket_id: str,
    current_user=Depends(
        get_current_user
    )
):

    if not ObjectId.is_valid(ticket_id):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket ID"
        )

    ticket = tickets_collection.find_one(
        {
            "_id": ObjectId(ticket_id)
        }
    )

    if ticket is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    if not can_access_ticket(
        ticket,
        current_user
    ):

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot access this ticket"
        )

    comments = comments_collection.find(
        {
            "ticket_id": ObjectId(ticket_id)
        }
    )

    return [
        comment_helper(comment)
        for comment in comments
    ]


# =========================================================
# 28. UPLOAD ATTACHMENT
# =========================================================


@app.post(
    "/tickets/{ticket_id}/attachments"
)
def upload_attachment(
    ticket_id: str,
    file: UploadFile = File(...),
    current_user=Depends(
        get_current_user
    )
):

    if not ObjectId.is_valid(ticket_id):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket ID"
        )

    ticket = tickets_collection.find_one(
        {
            "_id": ObjectId(ticket_id)
        }
    )

    if ticket is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    if not can_access_ticket(
        ticket,
        current_user
    ):

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot attach files to this ticket"
        )

    # Generate unique filename

    file_extension = ""

    if file.filename:

        file_extension = os.path.splitext(
            file.filename
        )[1]

    stored_filename = (
        f"{uuid.uuid4()}"
        f"{file_extension}"
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        stored_filename
    )

    # Save file

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    attachment_data = {

        "ticket_id": ObjectId(ticket_id),

        "original_filename":
            file.filename,

        "stored_filename":
            stored_filename,

        "content_type":
            file.content_type,

        "file_path":
            file_path,

        "uploaded_by":
            current_user["username"],

        "uploaded_at":
            datetime.now(
                timezone.utc
            ).isoformat()
    }

    result = attachments_collection.insert_one(
        attachment_data
    )

    create_audit_log(
        ticket_id,
        "ATTACHMENT_UPLOADED",
        current_user["username"],
        file.filename or ""
    )

    return {

        "id": str(result.inserted_id),

        "ticket_id": ticket_id,

        "filename": file.filename,

        "content_type":
            file.content_type,

        "uploaded_by":
            current_user["username"]
    }


# =========================================================
# 29. GET ATTACHMENTS
# =========================================================


@app.get(
    "/tickets/{ticket_id}/attachments"
)
def get_attachments(
    ticket_id: str,
    current_user=Depends(
        get_current_user
    )
):

    if not ObjectId.is_valid(ticket_id):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket ID"
        )

    ticket = tickets_collection.find_one(
        {
            "_id": ObjectId(ticket_id)
        }
    )

    if ticket is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    if not can_access_ticket(
        ticket,
        current_user
    ):

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot access this ticket"
        )

    attachments = attachments_collection.find(
        {
            "ticket_id": ObjectId(ticket_id)
        }
    )

    result = []

    for attachment in attachments:

        result.append(
            {
                "id":
                    str(attachment["_id"]),

                "filename":
                    attachment["original_filename"],

                "content_type":
                    attachment["content_type"],

                "uploaded_by":
                    attachment["uploaded_by"],

                "uploaded_at":
                    attachment["uploaded_at"]
            }
        )

    return result


# =========================================================
# 30. GET AUDIT LOG
# =========================================================


@app.get(
    "/tickets/{ticket_id}/audit"
)
def get_audit_logs(
    ticket_id: str,
    current_user=Depends(
        require_roles(
            TEAM_LEAD,
            ADMIN
        )
    )
):

    if not ObjectId.is_valid(ticket_id):

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket ID"
        )

    ticket = tickets_collection.find_one(
        {
            "_id": ObjectId(ticket_id)
        }
    )

    if ticket is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    logs = audit_logs_collection.find(
        {
            "ticket_id": ObjectId(ticket_id)
        }
    )

    result = []

    for log in logs:

        result.append(
            {
                "id":
                    str(log["_id"]),

                "ticket_id":
                    ticket_id,

                "action":
                    log["action"],

                "performed_by":
                    log["performed_by"],

                "details":
                    log["details"],

                "created_at":
                    log["created_at"]
            }
        )

    return result

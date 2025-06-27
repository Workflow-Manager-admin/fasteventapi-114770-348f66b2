from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# USER SCHEMAS


# PUBLIC_INTERFACE
class UserCreate(BaseModel):
    """Schema for registering a new user."""
    username: str = Field(..., description="Unique username")
    password: str = Field(..., min_length=4, description="Password")


# PUBLIC_INTERFACE
class UserShow(BaseModel):
    """Schema for user display (output)."""
    id: int
    username: str


# PUBLIC_INTERFACE
class Token(BaseModel):
    """Bearer token result."""
    access_token: str
    token_type: str = "bearer"


# EVENT SCHEMAS


# PUBLIC_INTERFACE
class EventCreate(BaseModel):
    """Input schema for creating events."""
    title: str
    description: Optional[str] = ""
    start_time: datetime
    end_time: datetime


# PUBLIC_INTERFACE
class EventShow(BaseModel):
    """Output schema for showing event details."""
    id: int
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    owner_id: int


# PUBLIC_INTERFACE
class EventUpdate(BaseModel):
    """Input schema for event updating."""
    title: Optional[str] = None
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

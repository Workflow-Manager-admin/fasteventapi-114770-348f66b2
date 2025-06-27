"""
FastAPI application for Event Manager: user authentication and event CRUD.
Uses JWT tokens for authenticated endpoints, Pydantic models for validation,
and modular routers for organization.

API summary:
- POST /auth/signup: Register a new user
- POST /auth/login: Obtain JWT token
- GET  /events: List all events (auth required)
- POST /events: Create a new event (auth required)
- GET  /events/{event_id}: Retrieve event details (auth required)
- PUT  /events/{event_id}: Update event (auth required, owner only)
- DELETE /events/{event_id}: Delete event (auth required, owner only)
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, events

app = FastAPI(
    title="Event Manager API",
    description="API for event management and user authentication.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Authentication", "description": "User sign up & login."},
        {"name": "Events", "description": "Event CRUD operations."}
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(events.router, prefix="/events", tags=["Events"])


@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

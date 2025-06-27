from fastapi import APIRouter, HTTPException, Depends
from typing import List

from ..schemas import (
    EventCreate,
    EventShow,
    EventUpdate,
    UserShow,
)
from ..services.auth_service import get_current_user
from ..services.event_service import (
    list_events,
    create_event,
    get_event,
    update_event,
    delete_event,
)

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/", response_model=List[EventShow], summary="List all events")
def get_events(current_user: UserShow = Depends(get_current_user)):
    """Retrieve all events for the authenticated user."""
    return list_events(current_user.id)


# PUBLIC_INTERFACE
@router.post("/", response_model=EventShow, status_code=201, summary="Create a new event")
def post_event(
    event: EventCreate,
    current_user: UserShow = Depends(get_current_user)
):
    """Create a new event for the current user."""
    return create_event(event, owner_id=current_user.id)


# PUBLIC_INTERFACE
@router.get("/{event_id}", response_model=EventShow, summary="Get event by ID")
def get_event_detail(
    event_id: int,
    current_user: UserShow = Depends(get_current_user)
):
    """Retrieve a single event by ID. Only owner can retrieve."""
    event = get_event(event_id)
    if not event or event.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Event not found.")
    return event


# PUBLIC_INTERFACE
@router.put("/{event_id}", response_model=EventShow, summary="Update an event")
def put_event(
    event_id: int,
    event_update: EventUpdate,
    current_user: UserShow = Depends(get_current_user)
):
    """Update an event (owner only)."""
    event = get_event(event_id)
    if not event or event.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Event not found or unauthorized.")
    return update_event(event_id, event_update)


# PUBLIC_INTERFACE
@router.delete("/{event_id}", status_code=204, summary="Delete an event")
def delete_event_route(
    event_id: int,
    current_user: UserShow = Depends(get_current_user)
):
    """Delete an event (owner only)."""
    event = get_event(event_id)
    if not event or event.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Event not found or unauthorized.")
    delete_event(event_id)
    return None

from typing import List, Optional

from ..schemas import (
    EventCreate,
    EventShow,
    EventUpdate,
)

# In-memory event store for demo only
events_db = {}
event_id_seq = 1


# PUBLIC_INTERFACE
def list_events(owner_id: int) -> List[EventShow]:
    """Return all events for the given user."""
    return [EventShow(**e) for e in events_db.values() if e["owner_id"] == owner_id]


# PUBLIC_INTERFACE
def create_event(event: EventCreate, owner_id: int) -> EventShow:
    global event_id_seq
    event_obj = {
        "id": event_id_seq,
        "title": event.title,
        "description": event.description or "",
        "start_time": event.start_time,
        "end_time": event.end_time,
        "owner_id": owner_id
    }
    events_db[event_id_seq] = event_obj
    event_id_seq += 1
    return EventShow(**event_obj)


# PUBLIC_INTERFACE
def get_event(event_id: int) -> Optional[EventShow]:
    e = events_db.get(event_id)
    if not e:
        return None
    return EventShow(**e)


# PUBLIC_INTERFACE
def update_event(event_id: int, event_update: EventUpdate) -> Optional[EventShow]:
    e = events_db.get(event_id)
    if not e:
        return None
    # Update only provided fields
    updated = dict(e)
    if event_update.title is not None:
        updated["title"] = event_update.title
    if event_update.description is not None:
        updated["description"] = event_update.description
    if event_update.start_time is not None:
        updated["start_time"] = event_update.start_time
    if event_update.end_time is not None:
        updated["end_time"] = event_update.end_time
    events_db[event_id] = updated
    return EventShow(**updated)


# PUBLIC_INTERFACE
def delete_event(event_id: int):
    if event_id in events_db:
        del events_db[event_id]

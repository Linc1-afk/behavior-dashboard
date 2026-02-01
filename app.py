from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI()

# In-memory event store
EVENTS = []

class Event(BaseModel):
    event_type: str
    description: str
    timestamp: datetime | None = None

    @app.get("/")
    def root():
        return{"status": "Backend is running"}
    
    @app.post("/event")
    def create_event(event: Event):
        event.timestamp = datetime.utcnow()
        EVENTS.append(event)
        return{"message": "Event received", "event": event}
    
    @app.get("/events")
    def get_events():
        return {
            "count": len(EVENTS),
            "events": EVENTS
        }
from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="Behavior Intelligence Engine")

EVENTS = []

@app.get("/")
def home():
    return {"status": "Behavior intelligence engine running"}

@app.post("/event")
def ingest_event(actor_id: str, event_type: str, raw_data: str):
    event = {
        "actor_id": actor_id,
        "event_type": event_type,
        "raw_data": raw_data,
        "risk_level": "HIGH",
        "message": "High risk behavior detected",
        "timestamp": datetime.utcnow().isoformat()
    }

    EVENTS.append(event)

    return {
        "status": "event received",
        "total_events": len(EVENTS),
        "event": event
    }

@app.get("/events_summary")
def events_summary():
    return {
        "total_events": len(EVENTS),
        "events": EVENTS
    }
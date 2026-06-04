from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.logger import logger
import hmac, hashlib
from app.core.config import settings

router = APIRouter()


def verify_signature(request_body: bytes, signature: str) -> bool:
    expected = hmac.new(
        settings.WEBHOOK_SECRET.encode(),
        request_body,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


@router.post("/hubspot")
async def hubspot_webhook(request: Request, db: Session = Depends(get_db)):
    """Receive real-time webhook events from HubSpot."""
    body = await request.body()
    signature = request.headers.get("X-HubSpot-Signature", "")

    if not verify_signature(body, signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    events = await request.json()
    logger.info(f"Received {len(events)} webhook event(s)")

    for event in events:
        object_type = event.get("objectType")
        event_type = event.get("subscriptionType")
        object_id = str(event.get("objectId"))
        logger.info(f"Event: {event_type} on {object_type} id={object_id}")
        # Extend here: trigger targeted re-sync for the affected record

    return {"received": len(events)}

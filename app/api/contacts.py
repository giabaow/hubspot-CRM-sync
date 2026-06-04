from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.sync_service import sync_contacts
from app.models.contact import Contact

router = APIRouter()


@router.post("/sync")
def trigger_contact_sync(db: Session = Depends(get_db)):
    """Manually trigger a contact sync from HubSpot."""
    result = sync_contacts(db)
    return {"message": "Contact sync complete", **result}


@router.get("/")
def list_contacts(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """List contacts stored in local DB."""
    contacts = db.query(Contact).offset(skip).limit(limit).all()
    return contacts

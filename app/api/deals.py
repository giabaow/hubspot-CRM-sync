from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.sync_service import sync_deals
from app.models.deal import Deal

router = APIRouter()


@router.post("/sync")
def trigger_deal_sync(db: Session = Depends(get_db)):
    """Manually trigger a deal sync from HubSpot."""
    result = sync_deals(db)
    return {"message": "Deal sync complete", **result}


@router.get("/")
def list_deals(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """List deals stored in local DB."""
    deals = db.query(Deal).offset(skip).limit(limit).all()
    return deals

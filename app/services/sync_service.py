from sqlalchemy.orm import Session
from app.services.hubspot_client import fetch_contacts, fetch_deals
from app.models.contact import Contact
from app.models.deal import Deal
from app.core.logger import logger


def sync_contacts(db: Session) -> dict:
    """Pull contacts from HubSpot and upsert into local DB."""
    records = fetch_contacts()
    created, updated = 0, 0

    for record in records:
        hubspot_id = record["id"]
        props = record.get("properties", {})

        existing = db.query(Contact).filter(Contact.hubspot_id == hubspot_id).first()
        if existing:
            for field in ["firstname", "lastname", "email", "company", "phone"]:
                setattr(existing, field, props.get(field))
            updated += 1
        else:
            db.add(Contact(
                hubspot_id=hubspot_id,
                firstname=props.get("firstname"),
                lastname=props.get("lastname"),
                email=props.get("email"),
                company=props.get("company"),
                phone=props.get("phone"),
            ))
            created += 1

    db.commit()
    logger.info(f"Contacts sync — created: {created}, updated: {updated}")
    return {"created": created, "updated": updated}


def sync_deals(db: Session) -> dict:
    """Pull deals from HubSpot and upsert into local DB."""
    records = fetch_deals()
    created, updated = 0, 0

    for record in records:
        hubspot_id = record["id"]
        props = record.get("properties", {})

        existing = db.query(Deal).filter(Deal.hubspot_id == hubspot_id).first()
        if existing:
            for field in ["dealname", "amount", "dealstage", "closedate", "pipeline"]:
                setattr(existing, field, props.get(field))
            updated += 1
        else:
            db.add(Deal(
                hubspot_id=hubspot_id,
                dealname=props.get("dealname"),
                amount=float(props["amount"]) if props.get("amount") else None,
                dealstage=props.get("dealstage"),
                closedate=props.get("closedate"),
                pipeline=props.get("pipeline"),
            ))
            created += 1

    db.commit()
    logger.info(f"Deals sync — created: {created}, updated: {updated}")
    return {"created": created, "updated": updated}

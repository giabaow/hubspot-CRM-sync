from fastapi import FastAPI
from app.api import contacts, deals, webhooks
from app.core.config import settings
from app.core.logger import logger

app = FastAPI(
    title="HubSpot CRM Sync Pipeline",
    description="Middleware service to sync HubSpot CRM data with internal PostgreSQL database",
    version="1.0.0",
)

app.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
app.include_router(deals.router, prefix="/deals", tags=["Deals"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "hubspot-crm-sync"}


@app.on_event("startup")
async def startup_event():
    logger.info("HubSpot CRM Sync service started")

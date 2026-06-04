import requests
from app.core.config import settings
from app.core.logger import logger

BASE_URL = "https://api.hubapi.com/crm/v3/objects"
HEADERS = {"Authorization": f"Bearer {settings.HUBSPOT_API_KEY}"}


def _get_all(object_type: str, properties: list[str]) -> list[dict]:
    """Fetch all records of a given CRM object type with pagination."""
    results = []
    url = f"{BASE_URL}/{object_type}"
    params = {"limit": 100, "properties": ",".join(properties)}

    while url:
        resp = requests.get(url, headers=HEADERS, params=params)
        resp.raise_for_status()
        data = resp.json()
        results.extend(data.get("results", []))
        paging = data.get("paging", {})
        url = paging.get("next", {}).get("link") if paging else None
        params = {}  # pagination link already contains params

    logger.info(f"Fetched {len(results)} {object_type} from HubSpot")
    return results


def fetch_contacts() -> list[dict]:
    return _get_all("contacts", ["firstname", "lastname", "email", "company", "phone"])


def fetch_deals() -> list[dict]:
    return _get_all("deals", ["dealname", "amount", "dealstage", "closedate", "pipeline"])


def create_contact(properties: dict) -> dict:
    resp = requests.post(f"{BASE_URL}/contacts", headers=HEADERS, json={"properties": properties})
    resp.raise_for_status()
    return resp.json()


def update_contact(hubspot_id: str, properties: dict) -> dict:
    resp = requests.patch(f"{BASE_URL}/contacts/{hubspot_id}", headers=HEADERS, json={"properties": properties})
    resp.raise_for_status()
    return resp.json()

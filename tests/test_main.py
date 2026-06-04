import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@patch("app.api.contacts.sync_contacts")
def test_contact_sync_endpoint(mock_sync):
    mock_sync.return_value = {"created": 5, "updated": 2}
    response = client.post("/contacts/sync")
    assert response.status_code == 200
    data = response.json()
    assert data["created"] == 5
    assert data["updated"] == 2


@patch("app.api.deals.sync_deals")
def test_deal_sync_endpoint(mock_sync):
    mock_sync.return_value = {"created": 3, "updated": 1}
    response = client.post("/deals/sync")
    assert response.status_code == 200
    data = response.json()
    assert data["created"] == 3


@patch("app.services.hubspot_client.requests.get")
def test_fetch_contacts_pagination(mock_get):
    """Test that pagination is handled correctly."""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "results": [{"id": "1", "properties": {"firstname": "John", "email": "j@test.com"}}],
        "paging": {}
    }
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    from app.services.hubspot_client import fetch_contacts
    contacts = fetch_contacts()
    assert len(contacts) == 1
    assert contacts[0]["id"] == "1"


def test_webhook_invalid_signature():
    response = client.post("/webhooks/hubspot", json=[{"objectType": "contact"}])
    assert response.status_code == 401

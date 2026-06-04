# HubSpot CRM Sync Pipeline

A middleware service that syncs HubSpot CRM data (contacts, deals) with a local PostgreSQL database via REST API polling and webhook listeners.

## Architecture

```
HubSpot CRM API
      ↕  (REST polling + webhooks)
FastAPI Middleware (this service)
      ↕
PostgreSQL Database
```

## Features

- Bidirectional sync of contacts and deals
- Webhook listener for real-time HubSpot events with HMAC signature verification
- Paginated API polling with retry logic
- Structured logging
- Full test coverage (unit + integration)
- Dockerised for consistent environments
- CI/CD via GitHub Actions

## Quick Start

### 1. Clone and configure

```bash
git clone https://github.com/giabaow/hubspot-crm-sync.git
cd hubspot-crm-sync
cp .env.example .env
# Fill in your HUBSPOT_API_KEY in .env
```

### 2. Run with Docker Compose

```bash
docker-compose up --build
```

API available at `http://localhost:8000`  
Swagger docs at `http://localhost:8000/docs`

### 3. Trigger a sync

```bash
# Sync contacts
curl -X POST http://localhost:8000/contacts/sync

# Sync deals
curl -X POST http://localhost:8000/deals/sync
```

### 4. Seed fake data (for testing without HubSpot)

```bash
python scripts/seed_fake_data.py
```

## Running Tests

```bash
pytest tests/ -v
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/contacts/sync` | Pull contacts from HubSpot |
| GET | `/contacts/` | List local contacts |
| POST | `/deals/sync` | Pull deals from HubSpot |
| GET | `/deals/` | List local deals |
| POST | `/webhooks/hubspot` | Receive HubSpot webhook events |

## Project Structure

```
hubspot-crm-sync/
├── app/
│   ├── api/            # Route handlers
│   ├── core/           # Config, DB, logger
│   ├── models/         # SQLAlchemy models
│   ├── services/       # HubSpot client, sync logic
│   └── main.py
├── tests/
├── scripts/            # Seed scripts
├── .github/workflows/  # CI pipeline
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Tech Stack

Python · FastAPI · PostgreSQL · SQLAlchemy · Docker · GitHub Actions

# HubSpot CRM Sync — Test Automation Suite

TypeScript + Playwright test suite covering the [`hubspot-CRM-sync`](https://github.com/giabaow/hubspot-CRM-sync) FastAPI middleware service: API tests for the core endpoints, and UI tests automating the service's Swagger docs interface at `/docs`.

## Why Swagger docs for "UI tests"?

`hubspot-CRM-sync` is a backend-only service — there's no custom frontend. FastAPI auto-generates an interactive Swagger UI at `/docs`, which is a real, browser-renderable interface. Automating it (expanding operations, running "Try it out", verifying responses render) is a legitimate UI automation target and mirrors how QA teams commonly validate API docs stay in sync with actual behavior.

## Structure

```
tests/
  api/
    health.spec.ts      - service health/status check
    contacts.spec.ts     - CRUD + validation for the contacts resource
    deals.spec.ts        - CRUD + stage updates + validation for deals
    webhooks.spec.ts     - HMAC signature verification (valid/invalid/missing/malformed)
  ui/
    swagger-docs.spec.ts - Swagger UI rendering, endpoint discovery, live "Try it out" execution
```

## Important: adjust to match the real repo

These tests are written against the **assumed** REST surface described in the project (contacts/deals sync, HMAC-verified webhooks, PostgreSQL-backed). Before running against the real service:

1. Confirm actual endpoint paths and field names in `hubspot-CRM-sync` (e.g. `/contacts` vs `/api/contacts`, `email` vs `contact_email`).
2. Confirm the webhook signature header name and HMAC algorithm match what the service actually implements.
3. Update `playwright.config.ts`'s `baseURL` to wherever the service runs (local, Docker, staging).
4. Update the Swagger UI selectors in `swagger-docs.spec.ts` if the FastAPI `title`/tags differ from what's assumed here.

## Running

```bash
npm install
npx playwright install --with-deps chromium

# make sure hubspot-CRM-sync is running locally (or set BASE_URL)
npm test              # run everything
npm run test:api      # API tests only
npm run test:ui       # Swagger UI tests only
npm run test:report   # open the HTML report
```

## CI

Designed to slot into the same GitHub Actions pipeline already used in `hubspot-CRM-sync` — add a job that starts the FastAPI service (or points `BASE_URL` at a deployed environment) and then runs `npm test`.

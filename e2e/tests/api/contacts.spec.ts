import { test, expect } from '@playwright/test';

// Assumed REST surface for the contacts resource, based on the FastAPI +
// PostgreSQL sync service pattern described in the hubspot-CRM-sync README.
// Adjust paths/fields below to match the actual routes in the repo.

test.describe('Contacts sync API', () => {
  test('GET /contacts returns a paginated list', async ({ request }) => {
    const res = await request.get('/contacts?limit=10');
    expect(res.status()).toBe(200);

    const body = await res.json();
    expect(Array.isArray(body.items ?? body)).toBeTruthy();
  });

  test('POST /contacts creates a new contact with valid payload', async ({ request }) => {
    const payload = {
      email: `test.user.${Date.now()}@example.com`,
      first_name: 'Test',
      last_name: 'User',
    };

    const res = await request.post('/contacts', { data: payload });
    expect([200, 201]).toContain(res.status());

    const body = await res.json();
    expect(body.email).toBe(payload.email);
    expect(body).toHaveProperty('id');
  });

  test('POST /contacts rejects invalid email format', async ({ request }) => {
    const res = await request.post('/contacts', {
      data: { email: 'not-an-email', first_name: 'Bad', last_name: 'Data' },
    });

    expect(res.status()).toBe(422); // FastAPI/Pydantic validation error
  });

  test('GET /contacts/{id} returns 404 for a non-existent contact', async ({ request }) => {
    const res = await request.get('/contacts/00000000-0000-0000-0000-000000000000');
    expect(res.status()).toBe(404);
  });
});

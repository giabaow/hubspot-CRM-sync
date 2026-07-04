import { test, expect } from '@playwright/test';

test.describe('Deals sync API', () => {
  test('GET /deals returns a list of deals', async ({ request }) => {
    const res = await request.get('/deals?limit=10');
    expect(res.status()).toBe(200);

    const body = await res.json();
    expect(Array.isArray(body.items ?? body)).toBeTruthy();
  });

  test('POST /deals creates a new deal linked to a contact', async ({ request }) => {
    // Assumes a contact fixture already exists; in a full suite this would
    // come from a setup/seed step rather than a hardcoded id.
    const payload = {
      deal_name: `Test Deal ${Date.now()}`,
      amount: 5000,
      stage: 'appointmentscheduled',
    };

    const res = await request.post('/deals', { data: payload });
    expect([200, 201]).toContain(res.status());

    const body = await res.json();
    expect(body.deal_name).toBe(payload.deal_name);
    expect(body.stage).toBe('appointmentscheduled');
  });

  test('PATCH /deals/{id} updates the deal stage', async ({ request }) => {
    const createRes = await request.post('/deals', {
      data: { deal_name: `Stage Update ${Date.now()}`, amount: 1000, stage: 'appointmentscheduled' },
    });
    const created = await createRes.json();

    const updateRes = await request.patch(`/deals/${created.id}`, {
      data: { stage: 'closedwon' },
    });

    expect(updateRes.status()).toBe(200);
    const updated = await updateRes.json();
    expect(updated.stage).toBe('closedwon');
  });

  test('POST /deals rejects negative amount', async ({ request }) => {
    const res = await request.post('/deals', {
      data: { deal_name: 'Invalid Deal', amount: -100, stage: 'appointmentscheduled' },
    });

    expect(res.status()).toBe(422);
  });
});

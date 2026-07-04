import { test, expect } from '@playwright/test';
import * as crypto from 'crypto';

// The hubspot-CRM-sync service verifies inbound HubSpot webhooks using an
// HMAC signature. These tests cover the signature verification path, which
// is the highest-risk part of any webhook receiver.

const WEBHOOK_SECRET = process.env.HUBSPOT_WEBHOOK_SECRET || 'test-secret';

function signPayload(body: string, secret: string): string {
  return crypto.createHmac('sha256', secret).update(body).digest('hex');
}

test.describe('HubSpot webhook receiver', () => {
  test('accepts a webhook with a valid HMAC signature', async ({ request }) => {
    const payload = JSON.stringify([
      { subscriptionType: 'contact.propertyChange', objectId: 12345, propertyName: 'email' },
    ]);
    const signature = signPayload(payload, WEBHOOK_SECRET);

    const res = await request.post('/webhooks/hubspot', {
      data: payload,
      headers: {
        'Content-Type': 'application/json',
        'X-HubSpot-Signature-V3': signature,
      },
    });

    expect(res.status()).toBe(200);
  });

  test('rejects a webhook with an invalid HMAC signature', async ({ request }) => {
    const payload = JSON.stringify([{ subscriptionType: 'contact.propertyChange', objectId: 12345 }]);

    const res = await request.post('/webhooks/hubspot', {
      data: payload,
      headers: {
        'Content-Type': 'application/json',
        'X-HubSpot-Signature-V3': 'deliberately-wrong-signature',
      },
    });

    expect([401, 403]).toContain(res.status());
  });

  test('rejects a webhook missing the signature header entirely', async ({ request }) => {
    const payload = JSON.stringify([{ subscriptionType: 'deal.propertyChange', objectId: 999 }]);

    const res = await request.post('/webhooks/hubspot', {
      data: payload,
      headers: { 'Content-Type': 'application/json' },
    });

    expect([401, 403]).toContain(res.status());
  });

  test('rejects a malformed payload with a valid signature', async ({ request }) => {
    const payload = '{not-valid-json';
    const signature = signPayload(payload, WEBHOOK_SECRET);

    const res = await request.post('/webhooks/hubspot', {
      data: payload,
      headers: {
        'Content-Type': 'application/json',
        'X-HubSpot-Signature-V3': signature,
      },
    });

    expect(res.status()).toBe(422);
  });
});

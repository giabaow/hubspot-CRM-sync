import { test, expect } from '@playwright/test';

test.describe('Health / status endpoint', () => {
  test('GET /health returns 200 and healthy status', async ({ request }) => {
    const res = await request.get('/health');
    expect(res.status()).toBe(200);

    const body = await res.json();
    expect(body).toHaveProperty('status');
    expect(['ok', 'healthy', 'up']).toContain(body.status?.toLowerCase());
  });

  test('service responds within acceptable latency', async ({ request }) => {
    const start = Date.now();
    const res = await request.get('/health');
    const elapsed = Date.now() - start;

    expect(res.status()).toBe(200);
    expect(elapsed).toBeLessThan(1000);
  });
});

import { defineConfig } from '@playwright/test';

// NOTE: adjust baseURL to match wherever your hubspot-CRM-sync FastAPI service
// is actually running (local dev, Docker container, or staging deployment).
export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  retries: 1,
  reporter: [['html', { open: 'never' }], ['list']],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:8000',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [
    {
      name: 'api',
      testMatch: /tests\/api\/.*\.spec\.ts/,
    },
    {
      name: 'ui-chromium',
      testMatch: /tests\/ui\/.*\.spec\.ts/,
      use: { browserName: 'chromium' },
    },
  ],
});

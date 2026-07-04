import { test, expect } from '@playwright/test';

// FastAPI auto-generates an interactive Swagger UI at /docs. Since
// hubspot-CRM-sync is a backend-only service with no custom frontend, this
// is the real, testable UI surface for the project — and it's a legitimate
// target for browser automation (many QA teams do exactly this).

test.describe('Swagger UI (/docs)', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/docs');
  });

  test('docs page loads with correct title and API name', async ({ page }) => {
    await expect(page).toHaveTitle(/Swagger UI/i);
    await expect(page.locator('.title')).toContainText(/hubspot/i);
  });

  test('all expected endpoint groups are listed', async ({ page }) => {
    const expectedTags = ['contacts', 'deals', 'webhooks'];

    for (const tag of expectedTags) {
      await expect(page.locator(`#operations-tag-${tag}`)).toBeVisible();
    }
  });

  test('can expand the GET /contacts operation and see parameters', async ({ page }) => {
    const contactsGroup = page.locator('#operations-tag-contacts');
    await contactsGroup.click();

    const getContacts = page.locator('.opblock-get', { hasText: '/contacts' }).first();
    await getContacts.click();

    await expect(getContacts.locator('.opblock-description')).toBeVisible();
    await expect(getContacts.getByText('Parameters')).toBeVisible();
  });

  test('"Try it out" executes a live request and shows a response', async ({ page }) => {
    const contactsGroup = page.locator('#operations-tag-contacts');
    await contactsGroup.click();

    const getContacts = page.locator('.opblock-get', { hasText: '/contacts' }).first();
    await getContacts.click();

    await getContacts.getByRole('button', { name: 'Try it out' }).click();
    await getContacts.getByRole('button', { name: 'Execute' }).click();

    const responseSection = getContacts.locator('.responses-wrapper');
    await expect(responseSection).toBeVisible();
    await expect(responseSection.getByText(/Response body/i)).toBeVisible();
  });
});

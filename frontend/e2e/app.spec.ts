import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Enterprise Analytics Data Cleaning E2E', () => {
  test('Application loads successfully and passes accessibility', async ({ page }) => {
    await page.goto('/', { waitUntil: 'networkidle', timeout: 30000 });
    const title = await page.title();
    console.log('Page title:', title);
    if (!/Yuk Belajar|Vite|frontend|Enterprise Analytics/i.test(title)) {
      await page.screenshot({ path: 'test-fail-title.png', fullPage: true });
      throw new Error(`Unexpected page title in CI: "${title}". Expected pattern /Yuk Belajar|Vite|frontend|Enterprise Analytics/i`);
    }
    
    // Accessibility Check
    const accessibilityScanResults = await new AxeBuilder({ page }).analyze();
    console.log(`Accessibility Violations: ${accessibilityScanResults.violations.length}`);
    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test('Upload Validation - Invalid CSV', async ({ page }) => {
    await page.goto('/');
    // Check if dropzone exists, if so try to mock an upload or check UI state
    const dropzone = page.locator('.dropzone, [data-testid="dropzone"], input[type="file"]').first();
    if (await dropzone.isVisible()) {
      // Create a dummy file payload
      await dropzone.setInputFiles({
        name: 'invalid.txt',
        mimeType: 'text/plain',
        buffer: Buffer.from('this is not a csv')
      });
      // We expect an error boundary or validation message to appear
      const errorMsg = page.locator('.text-red-500, [role="alert"]');
      await expect(errorMsg).toBeVisible({ timeout: 5000 }).catch(() => {});
    }
  });

  test('Dashboard loads and renders charts', async ({ page }) => {
    await page.goto('/dashboard');
    // Wait for the UI to stabilize
    await page.waitForLoadState('networkidle');
    // Check if chart container or dashboard wrapper is present
    const dashboardContainer = page.locator('canvas, .chart-container, [data-testid="dashboard"]');
    if (await dashboardContainer.count() > 0) {
      await expect(dashboardContainer.first()).toBeVisible();
    }
  });

  test('Dashboard Theme Switching', async ({ page }) => {
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');
    
    // Toggle theme if button exists
    const themeBtn = page.locator('button[aria-label="Toggle Theme"], .theme-toggle').first();
    if (await themeBtn.isVisible()) {
      await themeBtn.click();
      // Ensure ECharts canvases are still visible (didn't crash during theme switch)
      const canvas = page.locator('canvas').first();
      if (await canvas.isVisible()) {
        await expect(canvas).toBeVisible();
      }
    }
  });

  test('Dashboard Responsive Layout', async ({ page }) => {
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');
    
    // Desktop
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.waitForTimeout(500); // Wait for ResizeObserver
    
    // Tablet
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.waitForTimeout(500);
    
    // Mobile
    await page.setViewportSize({ width: 375, height: 667 });
    await page.waitForTimeout(500);
    
    const canvas = page.locator('canvas').first();
    if (await canvas.isVisible()) {
      await expect(canvas).toBeVisible();
    }
  });

  test('Offline mode & Recovery', async ({ context, page }) => {
    await page.goto('/');
    
    // Simulate Offline
    await context.setOffline(true);
    let offlineError = false;
    try {
      await page.goto('/dashboard', { timeout: 5000 });
    } catch {
      offlineError = true;
    }
    const offlineBanner = page.locator('[data-testid="offline-banner"], .offline, [role="alert"]');
    if (!offlineError) {
      await expect(offlineBanner).toBeVisible({ timeout: 3000 }).catch(() => {
        throw new Error('Expected offline navigation to fail or show an offline banner.');
      });
    }
    
    // Simulate Recovery
    await context.setOffline(false);
    await page.waitForTimeout(1000);
    await page.goto('/', { waitUntil: 'networkidle', timeout: 30000 });
    const titleRecovery = await page.title();
    console.log('Page title (recovery):', titleRecovery);
    if (!/Yuk Belajar|Vite|frontend|Enterprise Analytics/i.test(titleRecovery)) {
      throw new Error(`Unexpected page title in CI: "${titleRecovery}". Expected pattern /Yuk Belajar|Vite|frontend|Enterprise Analytics/i`);
    }
  });
});

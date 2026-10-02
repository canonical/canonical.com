import { expect, test } from "@playwright/test";
import { acceptCookiePolicy } from "../../helpers/navigation-helpers";

test("Ubuntu Pro description fits mobile, tablet, and desktop viewports", async ({
  page,
}) => {
  await page.setViewportSize({ width: 320, height: 700 });
  await page.goto("/legal/ubuntu-pro-description");
  await expect(
    page.getByRole("heading", { name: "Ubuntu Pro Description" })
  ).toBeVisible();

  for (const width of [320, 375, 390, 768, 1280]) {
    await page.setViewportSize({ width, height: 700 });
    const scrollWidth = await page.evaluate(
      () => document.documentElement.scrollWidth
    );
    expect(scrollWidth, `page overflows at ${width}px`).toBeLessThanOrEqual(
      width
    );

    if (width === 320) {
      const longUrl = page
        .locator(".p-legal-content a")
        .filter({ hasText: "https://github.com/orgs/canonical/packages" });
      await expect(longUrl).toBeVisible();
      const wrapMetrics = await longUrl.evaluate((link) => {
        const container = link.closest("li, p") as HTMLElement | null;
        return {
          lines: link.getClientRects().length,
          clientWidth: container?.clientWidth ?? 0,
          scrollWidth: container?.scrollWidth ?? 0,
        };
      });
      expect(wrapMetrics.lines).toBeGreaterThan(1);
      expect(wrapMetrics.scrollWidth).toBeLessThanOrEqual(
        wrapMetrics.clientWidth
      );

      const tableWidths = await page
        .locator(".p-sev-table-wrap")
        .evaluate((wrapper) => ({
          visible: wrapper.clientWidth,
          content: wrapper.scrollWidth,
        }));
      expect(tableWidths.content).toBeGreaterThan(tableWidths.visible);
    }
  }
});

test("PDF export dialog stays usable on a narrow screen", async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 568 });
  await page.goto("/legal/ubuntu-pro-description");
  await acceptCookiePolicy(page);

  await page.getByRole("button", { name: "Export to PDF" }).click();
  const dialog = page.locator("#export-pdf-modal .p-modal__dialog");
  await expect(dialog).toBeVisible();

  const bounds = await dialog.boundingBox();
  expect(bounds).not.toBeNull();
  expect(bounds!.x).toBeGreaterThanOrEqual(0);
  expect(bounds!.x + bounds!.width).toBeLessThanOrEqual(320);

  const exportButton = dialog.getByRole("button", { name: "Export" });
  await exportButton.scrollIntoViewIfNeeded();
  await expect(exportButton).toBeVisible();
  await expect(exportButton).toBeEnabled();
  const exportBounds = await exportButton.boundingBox();
  expect(exportBounds).not.toBeNull();
  expect(exportBounds!.x + exportBounds!.width).toBeLessThanOrEqual(320);
  expect(exportBounds!.y + exportBounds!.height).toBeLessThanOrEqual(568);
  await exportButton.click({ trial: true });
  await page.keyboard.press("Escape");
  await expect(dialog).not.toBeVisible();
});

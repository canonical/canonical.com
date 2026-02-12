import { test, expect } from "@playwright/test";
import { navigateToHomepage } from "../../helpers/navigation-helpers";
import {
  clearDataLayer,
  getDataLayerEventsByName,
} from "../../helpers/datalayer-helpers";

const EVENT_NAME = "meganav click";

test.describe("meganav tracking - search", () => {
  test.beforeEach(async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await navigateToHomepage(page);
  });

  test("search toggle button pushes correct dataLayer event", async ({
    page,
  }) => {
    const searchToggle = page.locator("#js-search-button-desktop");
    await expect(searchToggle).toBeVisible();

    await clearDataLayer(page);
    await searchToggle.click();

    const events = await getDataLayerEventsByName(page, EVENT_NAME);
    expect(events.length).toBeGreaterThanOrEqual(1);

    // Clicking toggle also auto-focuses the input, so the toggle event is first
    const event = events[0];
    expect(event.mega_nav_area).toBe("search");
    expect(event.click_label).toBe("search toggle");
    expect(event.mega_nav_path).toBe("search toggle");
  });

  test("search input focus pushes correct dataLayer event", async ({
    page,
  }) => {
    // Open search first
    const searchToggle = page.locator("#js-search-button-desktop");
    await searchToggle.click();

    // Wait for search input to be visible
    const searchInput = page.locator(".p-search-box__input");
    await expect(searchInput).toBeVisible();

    // Blur the input first (it gets auto-focused when search opens)
    await searchInput.blur();
    await clearDataLayer(page);
    await searchInput.focus();

    const events = await getDataLayerEventsByName(page, EVENT_NAME);
    expect(events.length).toBeGreaterThanOrEqual(1);

    const event = events[events.length - 1];
    expect(event.mega_nav_area).toBe("search");
    expect(event.click_label).toBe("search input focused");
    expect(event.mega_nav_path).toBe("search input focused");
  });

  test("search reset button pushes correct dataLayer event", async ({
    page,
  }) => {
    // Open search
    const searchToggle = page.locator("#js-search-button-desktop");
    await searchToggle.click();

    // Type a query so the reset button becomes active
    const searchInput = page.locator(".p-search-box__input");
    await expect(searchInput).toBeVisible();
    await searchInput.fill("ubuntu");

    // Click the reset button
    const resetButton = page.locator(".p-search-box__reset");
    await expect(resetButton).toBeVisible();

    await clearDataLayer(page);
    await resetButton.click();

    const events = await getDataLayerEventsByName(page, EVENT_NAME);
    expect(events.length).toBeGreaterThanOrEqual(1);

    const event = events[events.length - 1];
    expect(event.mega_nav_area).toBe("search");
    expect(event.click_label).toBe("search reset");
    expect(event.mega_nav_path).toBe("search reset");
  });
});

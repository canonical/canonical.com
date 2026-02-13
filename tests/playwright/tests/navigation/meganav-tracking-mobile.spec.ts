import { test, expect } from "@playwright/test";
import { navigateToHomepage } from "../../helpers/navigation-helpers";
import {
  clearDataLayer,
  getDataLayerEventsByName,
} from "../../helpers/datalayer-helpers";

const EVENT_NAME = "meganav click mobile";

test.describe("meganav tracking - mobile", () => {
  test.beforeEach(async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await navigateToHomepage(page);
  });

  test("menu button open/close pushes correct dataLayer events", async ({
    page,
  }) => {
    const menuButton = page.locator(".js-menu-button");
    await expect(menuButton).toBeVisible();

    // Open menu
    await clearDataLayer(page);
    await menuButton.click();

    let events = await getDataLayerEventsByName(page, EVENT_NAME);
    expect(events.length).toBeGreaterThanOrEqual(1);

    let event = events[events.length - 1];
    expect(event.mega_nav_area).toBe("menu");
    expect(event.click_label).toBe("menu");
    expect(event.click_action).toBe("open");

    // Close menu
    await clearDataLayer(page);
    await menuButton.click();

    events = await getDataLayerEventsByName(page, EVENT_NAME);
    expect(events.length).toBeGreaterThanOrEqual(1);

    event = events[events.length - 1];
    expect(event.mega_nav_area).toBe("menu");
    expect(event.click_label).toBe("menu");
    expect(event.click_action).toBe("close");
  });

  test("top-level section toggle pushes correct dataLayer event", async ({
    page,
  }) => {
    // Open mobile menu
    const menuButton = page.locator(".js-menu-button");
    await menuButton.click();
    await expect(page.locator("#navigation")).toHaveClass(/has-menu-open/);

    // Click a top-level section (e.g., Products)
    const sectionToggle = page
      .locator(".js-dropdown-button[data-level='0']")
      .first();
    await expect(sectionToggle).toBeVisible();

    await clearDataLayer(page);
    await sectionToggle.click();

    const events = await getDataLayerEventsByName(page, EVENT_NAME);
    expect(events.length).toBeGreaterThanOrEqual(1);

    const event = events[events.length - 1];
    expect(event.mega_nav_area).toBe("level-1");
    expect(event.click_label).toBe("1. products");
    expect(event.mega_nav_path).toBe("1. products");
  });

  test("back button pushes correct dataLayer event", async ({ page }) => {
    // Open mobile menu
    const menuButton = page.locator(".js-menu-button");
    await menuButton.click();
    await expect(page.locator("#navigation")).toHaveClass(/has-menu-open/);

    // Open a section to make back button visible
    const sectionToggle = page
      .locator(".js-dropdown-button[data-level='0']")
      .first();
    await sectionToggle.click();

    // Wait for the back button to be visible
    const backButton = page.locator(".js-back-button").first();
    await expect(backButton).toBeVisible();

    await clearDataLayer(page);
    await backButton.click();

    const events = await getDataLayerEventsByName(page, EVENT_NAME);
    expect(events.length).toBeGreaterThanOrEqual(1);

    const event = events[events.length - 1];
    expect(event.mega_nav_area).toMatch(/^level-\d+$/);
    expect(event.click_label).toBe("back");
  });

  test("nested section toggle (level-2) pushes correct dataLayer event", async ({
    page,
  }) => {
    // Open mobile menu
    const menuButton = page.locator(".js-menu-button");
    await menuButton.click();
    await expect(page.locator("#navigation")).toHaveClass(/has-menu-open/);

    // Open Products section
    const sectionToggle = page
      .locator(".js-dropdown-button[data-level='0']")
      .first();
    await sectionToggle.click();

    // Wait for nested section toggles to be visible
    const nestedToggle = page
      .locator(".js-dropdown-button[data-level='1']")
      .first();
    await expect(nestedToggle).toBeVisible();

    await clearDataLayer(page);
    await nestedToggle.click();

    const events = await getDataLayerEventsByName(page, EVENT_NAME);
    expect(events.length).toBeGreaterThanOrEqual(1);

    const event = events[events.length - 1];
    expect(event.mega_nav_area).toBe("level-2");
    expect(event.click_label).toMatch(/^\d+\. .+/);
    expect(event.mega_nav_path).toContain("1. products");
    expect(event.mega_nav_path).toContain(" | ");
  });

  test("link click (level-3) pushes event with click_from and click_to", async ({
    page,
  }) => {
    // Open mobile menu
    const menuButton = page.locator(".js-menu-button");
    await menuButton.click();
    await expect(page.locator("#navigation")).toHaveClass(/has-menu-open/);

    // Open Products section
    const sectionToggle = page
      .locator(".js-dropdown-button[data-level='0']")
      .first();
    await sectionToggle.click();

    // Open a nested section so its links become visible and clickable
    const nestedToggle = page
      .locator(".js-dropdown-button[data-level='1']")
      .first();
    await expect(nestedToggle).toBeVisible();
    await nestedToggle.click();

    // Find an external link inside the open nested section
    const navLink = page
      .locator(
        "#products-content .p-navigation__dropdown-content--sliding a:not(.js-back-button):not(.js-dropdown-button):not([href^='#'])"
      )
      .first();
    await expect(navLink).toBeVisible();

    await clearDataLayer(page);

    // Click the link and capture the dataLayer event atomically to avoid navigation context loss
    const event = await navLink.evaluate((el, eventName) => {
      // Prevent default to stop navigation, using capture phase to run first
      el.addEventListener("click", (e) => e.preventDefault(), {
        once: true,
        capture: true,
      });
      (el as HTMLElement).click();
      // Read dataLayer synchronously right after the click handlers fire
      const dl = (window as any).dataLayer || [];
      const events = dl.filter(
        (e: any) => e.event === eventName
      );
      return events[events.length - 1] || null;
    }, EVENT_NAME);

    expect(event).toBeTruthy();
    expect(event.mega_nav_area).toBe("level-3");
    expect(event.click_label).toMatch(/^\d+\. .+/);
    // mega_nav_path contains pipe-separated segments ending with the click_label
    expect(event.mega_nav_path).toContain(event.click_label as string);
    expect(event.click_from).toBeTruthy();
    expect(event.click_to).toBeTruthy();
  });
});

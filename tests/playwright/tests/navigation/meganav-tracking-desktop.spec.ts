import { test, expect } from "@playwright/test";
import { navigateToHomepage } from "../../helpers/navigation-helpers";
import {
  clearDataLayer,
  getDataLayerEventsByName,
} from "../../helpers/datalayer-helpers";

const EVENT_NAME = "meganav click desktop";

test.describe("meganav tracking - desktop", () => {
  test.beforeEach(async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await navigateToHomepage(page);
  });

  test("topbar click pushes correct dataLayer event", async ({ page }) => {
    await clearDataLayer(page);

    const productsButton = page.locator(
      '.js-dropdown-button[data-level="0"][aria-controls="products-content"]'
    );
    await productsButton.click();

    const events = await getDataLayerEventsByName(page, EVENT_NAME);
    expect(events.length).toBeGreaterThanOrEqual(1);

    const event = events[events.length - 1];
    expect(event.mega_nav_area).toBe("topbar");
    expect(event.click_label).toBe("1. products");
    expect(event.mega_nav_path).toBe("1. products");
  });

  test("sidebar tab click pushes correct dataLayer event", async ({
    page,
  }) => {
    // Open Products dropdown first
    const productsButton = page.locator(
      '.js-dropdown-button[data-level="0"][aria-controls="products-content"]'
    );
    await productsButton.click();
    await expect(page.locator("#products-content")).toBeVisible();

    // Find a sidebar tab to click
    const sidebarTab = page
      .locator("#products-content .js-navigation-tab")
      .first();
    await expect(sidebarTab).toBeVisible();

    await clearDataLayer(page);
    await sidebarTab.click();

    const events = await getDataLayerEventsByName(page, EVENT_NAME);
    expect(events.length).toBeGreaterThanOrEqual(1);

    const event = events[events.length - 1];
    expect(event.mega_nav_area).toBe("sidebar");
    expect(event.click_label).toMatch(/^\d+\. .+/);
    expect(event.mega_nav_path).toContain("1. products");
    expect(event.mega_nav_path).toContain(" | ");

    // The click_label should appear as the last segment of the path
    expect(event.mega_nav_path).toContain(event.click_label as string);
  });

  test("dropdown link click pushes event with click_from and click_to", async ({
    page,
  }) => {
    // Open Products dropdown
    const productsButton = page.locator(
      '.js-dropdown-button[data-level="0"][aria-controls="products-content"]'
    );
    await productsButton.click();
    await expect(page.locator("#products-content")).toBeVisible();

    // Find a visible link inside the dropdown window (not the mobile sliding panel)
    const dropdownLink = page
      .locator(
        "#products-content .js-dropdown-window a.p-navigation__dropdown-item, #products-content .js-dropdown-window .p-navigation__link-list a, #products-content .js-dropdown-window a.p-navigation__preview-link"
      )
      .first();
    await expect(dropdownLink).toBeVisible();

    await clearDataLayer(page);

    // Click the link and capture the dataLayer event atomically to avoid navigation context loss
    const event = await dropdownLink.evaluate((el, eventName) => {
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
    expect(event.mega_nav_area).toBe("topbar");
    expect(event.click_label).toMatch(/^\d+\. .+/);
    expect(event.mega_nav_path).toContain("1. products");
    expect(event.click_from).toBeTruthy();
    expect(event.click_to).toBeTruthy();
  });
});

import { expect, Page } from "@playwright/test";

declare global {
  interface Window {
    dataLayer: Record<string, unknown>[];
  }
}

/**
 * Get all dataLayer events from the page.
 */
export const getDataLayerEvents = async (
  page: Page
): Promise<Record<string, unknown>[]> => {
  return await page.evaluate(() => window.dataLayer || []);
};

/**
 * Get the most recent event from the dataLayer.
 */
export const getLastDataLayerEvent = async (
  page: Page
): Promise<Record<string, unknown> | undefined> => {
  return await page.evaluate(() => {
    const dl = window.dataLayer || [];
    return dl[dl.length - 1];
  });
};

/**
 * Reset the dataLayer to isolate events between interactions.
 */
export const clearDataLayer = async (page: Page): Promise<void> => {
  await page.evaluate(() => {
    if (!Array.isArray(window.dataLayer)) {
      window.dataLayer = [];
    }
    window.dataLayer.length = 0;
  });
};

/**
 * Wait for an event to be pushed before returning matching dataLayer events.
 */
export const waitForDataLayerEventsByName = async (
  page: Page,
  eventName: string
): Promise<Record<string, unknown>[]> => {
  await expect
    .poll(async () =>
      page.evaluate(
        (name) => (window.dataLayer || []).filter((event) => event.event === name).length,
        eventName
      )
    )
    .toBeGreaterThan(0);
  return page.evaluate(
    (name) => (window.dataLayer || []).filter((event) => event.event === name),
    eventName
  );
};

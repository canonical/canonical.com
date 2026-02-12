import { Page } from "@playwright/test";

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
    window.dataLayer = [];
  });
};

/**
 * Filter dataLayer events by the `event` field name.
 */
export const getDataLayerEventsByName = async (
  page: Page,
  eventName: string
): Promise<Record<string, unknown>[]> => {
  return await page.evaluate((name) => {
    return (window.dataLayer || []).filter((e) => e.event === name);
  }, eventName);
};

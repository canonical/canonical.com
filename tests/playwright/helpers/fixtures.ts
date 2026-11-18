import { test as base, expect } from "@playwright/test";
import { blockExternalRequests } from "./network";

export const test = base.extend({
  context: async ({ context, baseURL }, use) => {
    await blockExternalRequests(context, baseURL);
    await use(context);
  },
});

export { expect };

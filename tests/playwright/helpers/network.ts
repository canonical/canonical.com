import type { BrowserContext, Route } from "@playwright/test";

/**
 * Cross-origin paths that tests assert on and so must reach the real network.
 * The forms post to https://ubuntu.com/marketo/submit, and the form tests
 * assert on both the resulting URL and its status code.
 */
const ALLOWED_EXTERNAL_PATHS = ["/marketo/submit"];

/**
 * Mocks out every network request that does not target the given baseURL, so
 * that tests never depend on the real network. Third-party resources
 * (assets.ubuntu.com, Google Tag Manager, Cloudinary, YouTube…) are slow or
 * unreachable from CI and are the main reason navigations time out while
 * waiting for the "load" event.
 */
export async function blockExternalRequests(
  context: BrowserContext,
  baseURL?: string
): Promise<void> {
  const allowedOrigin = baseURL ? new URL(baseURL).origin : undefined;

  await context.route("**/*", (route: Route) => {
    const url = new URL(route.request().url());

    if (
      (allowedOrigin && url.origin === allowedOrigin) ||
      ALLOWED_EXTERNAL_PATHS.includes(url.pathname)
    ) {
      return route.continue();
    }

    // Empty 200 rather than abort: most of these are <script> and <img>
    // tags, and an aborted request surfaces as a page error.
    return route.fulfill({
      status: 200,
      contentType: "text/plain",
      body: "",
    });
  });
}

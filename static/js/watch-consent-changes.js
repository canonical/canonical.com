/*
  This script watches for changes to the cookie consent status and
  stores or clears the initial referrer and URL in sessionStorage
  based on whether consent has been given.
*/

/**
 * @typedef {Object} CookieChangeEvent
 * @property {Array<{name: string}>} changed
 */

/**
 * @typedef {Object} CookieStore
 * @property {(event: string, callback: (event: CookieChangeEvent) => void) => void} addEventListener
 */

/**
 * @type {Window & typeof globalThis & {cookieStore?: CookieStore}}
 */
const windowWithCookieStore = window;

const initialReferrerKey = "canonical.initialReferrer";
const initialUrlKey = "canonical.initialUrl";
let hasStoredSessionValues = false;

function stripReferrer(url) {
  if (!url) {
    return "";
  }
  try {
    const parsed = new URL(url, window.location.href);
    return parsed.origin || "";
  } catch (error) {
    return "";
  }
}

function getCookie(name) {
  const pattern = new RegExp("(^| )" + name + "=([^;]+)");
  const match = document.cookie.match(pattern);
  return match ? match[2] : null;
}

function hasConsent() {
  try {
    const value = getCookie("_cookies_accepted");
    return ["all", "performance"].includes(value);
  } catch {
    return false;
  }
}

function storeSessionValues() {
  if (hasStoredSessionValues) {
    return true;
  }
  try {
    if (!sessionStorage.getItem(initialReferrerKey)) {
      const refDomain = stripReferrer(document.referrer);
      if (refDomain) {
        sessionStorage.setItem(initialReferrerKey, refDomain);
      }
    }

    if (!sessionStorage.getItem(initialUrlKey)) {
      sessionStorage.setItem(initialUrlKey, window.location.href);
    }

    hasStoredSessionValues = true;
    return true;
  } catch {
    return false;
  }
}

function clearSessionValues() {
  try {
    sessionStorage.removeItem(initialReferrerKey);
    sessionStorage.removeItem(initialUrlKey);
  } catch {}
  hasStoredSessionValues = false;
}

function watchConsentChanges() {
  if (windowWithCookieStore.cookieStore && (windowWithCookieStore.cookieStore).addEventListener) {
    const handleChange = (event) => {
      const changed = (event.changed || []).some(
        (cookie) => cookie.name === "_cookies_accepted"
      );
      if (!changed) {
        return;
      }

      if (hasConsent()) {
        storeSessionValues();
      } else {
        clearSessionValues();
      }
    };

    (windowWithCookieStore.cookieStore).addEventListener("change", handleChange);
  }

  if (hasConsent()) {
    storeSessionValues();
  } else {
    clearSessionValues();
  }
}

watchConsentChanges();

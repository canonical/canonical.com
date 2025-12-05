import { Page, expect } from "@playwright/test";

/**
 * Navigation test helper functions for Canonical.com e2e tests
 */

export interface NavigationItem {
  title: string;
  url?: string;
  selector?: string;
  hasDropdown?: boolean;
}

export interface ViewportSize {
  width: number;
  height: number;
  name: string;
}

// Common viewport sizes for responsive testing
export const VIEWPORTS: ViewportSize[] = [
  { width: 1920, height: 1080, name: "Desktop Large" },
  { width: 1366, height: 768, name: "Desktop Standard" },
  { width: 1024, height: 768, name: "Tablet Landscape" },
  { width: 768, height: 1024, name: "Tablet Portrait" },
  { width: 375, height: 667, name: "Mobile" },
  { width: 320, height: 568, name: "Mobile Small" }
];

// Primary navigation items based on navigation.yaml analysis
export const PRIMARY_NAV_ITEMS: NavigationItem[] = [
  { title: "Products", selector: "#products-nav", hasDropdown: true },
  { title: "Solutions", selector: "#solutions-nav", hasDropdown: true },
  { title: "Partners", selector: "#partners-nav", hasDropdown: true },
  { title: "Careers", selector: "#careers-nav", hasDropdown: true },
  { title: "Company", selector: "#company-nav", hasDropdown: true }
];

export const MOBILE_THRESHOLD = 1035;

/**
 * Check if an element exists and is visible on the page
 */
export const isElementVisible = async (page: Page, selector: string): Promise<boolean> => {
  try {
    const element = page.locator(selector);
    return await element.isVisible();
  } catch {
    return false;
  }
};

/**
 * Accept cookie policy if present
 */
export const acceptCookiePolicy = async (page: Page): Promise<void> => {
  if (await isElementVisible(page, '#cookie-policy-button-accept-all')) {
    await page.locator('#cookie-policy-button-accept-all').click();
    // Wait for cookie banner to disappear
    await expect(page.locator('#cookie-policy-button-accept-all')).not.toBeVisible();
  }
};

/**
 * Check if we're on mobile viewport (width < MOBILE_THRESHOLD)
 */
export const isMobileViewport = async (page: Page): Promise<boolean> => {
  const viewport = page.viewportSize();
  return viewport ? viewport.width < MOBILE_THRESHOLD : false;
};

/**
 * Open mobile menu if on mobile viewport
 */
export const toggleMobileMenuIfNeeded = async (page: Page): Promise<void> => {
  if (await isMobileViewport(page)) {
    const menuButton = page.locator('.js-menu-button');
    if (await menuButton.isVisible()) {
      await menuButton.click();
    }
  }
};

/**
 * Click on a navigation item
 */
export const clickNavigationItem = async (page: Page, selector: string): Promise<void> => {
  const navItem = page.locator(selector);
  await navItem.click();
};

/**
 * Check if dropdown is open for a navigation item
 */
export const isDropdownOpen = async (page: Page, navItemId: string): Promise<boolean> => {
  const dropdownContent = page.locator(`#${navItemId.replace('-nav', '-content')}`).first();
  return await dropdownContent.isVisible();
};

/**
 * Get all visible links in a dropdown
 */
export const getDropdownLinks = async (page: Page, navItemId: string): Promise<string[]> => {
  const dropdownContent = page.locator(`#${navItemId.replace('-nav', '-content')}`);
  const links = dropdownContent.locator('a[href]');
  const linkTexts: string[] = [];
  
  const count = await links.count();
  for (let i = 0; i < count; i++) {
    const text = await links.nth(i).textContent();
    if (text?.trim()) {
      linkTexts.push(text.trim());
    }
  }
  
  return linkTexts;
};

/**
 * Test search functionality
 */
export const clickSearchButton = async (page: Page): Promise<void> => {
  const searchButton = page.locator((await isMobileViewport(page)) ? '#js-search-button-mobile' : '#js-search-button-desktop');
  await searchButton.click();
};

export const testSearchFunctionality = async (page: Page, searchTerm: string = "ubuntu"): Promise<void> => {
  // Open search
  await clickSearchButton(page);
  
  // Wait for search input to be visible
  await page.waitForSelector('#navigation-search', { state: 'visible' });
  
  // Type search term
  await page.fill('#navigation-search', searchTerm);
  
  // Submit search
  const searchButton = page.locator('.p-search-box__button');
  await searchButton.click();
  
  // Wait for navigation to search results
  await page.waitForURL('**/search**');
};

/**
 * Check if secondary navigation is present
 */
export const hasSecondaryNavigation = async (page: Page): Promise<boolean> => {
  return await isElementVisible(page, '#secondary-navigation');
};

/**
 * Get secondary navigation items
 */
export const getSecondaryNavigationItems = async (page: Page): Promise<string[]> => {
  if (!(await hasSecondaryNavigation(page))) {
    return [];
  }
  
  const secondaryNav = page.locator('#secondary-navigation .p-navigation__items a');
  const items: string[] = [];
  
  const count = await secondaryNav.count();
  for (let i = 0; i < count; i++) {
    const text = await secondaryNav.nth(i).textContent();
    if (text?.trim()) {
      items.push(text.trim());
    }
  }
  
  return items;
};

/**
 * Navigate to homepage and ensure clean state
 */
export const navigateToHomepage = async (page: Page): Promise<void> => {
  await page.goto('/');
  await acceptCookiePolicy(page);
};

/**
 * Check if page has loaded successfully
 */
export const verifyPageLoad = async (page: Page, expectedUrl?: string): Promise<void> => {
  // Check that page has loaded
  await page.waitForLoadState('domcontentloaded');
  
  // Verify URL if provided
  if (expectedUrl) {
    await expect(page).toHaveURL(new RegExp(expectedUrl));
  }
  
  // Check that main content is visible
  await expect(page.locator('main, .main-content, body')).toBeVisible();
};
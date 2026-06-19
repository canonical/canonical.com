import { test, expect } from "@playwright/test";
import {
  PRIMARY_NAV_ITEMS,
  VIEWPORTS,
  acceptCookiePolicy,
  navigateToHomepage,
  isMobileViewport,
  toggleMobileMenuIfNeeded,
  clickNavigationItem,
  isDropdownOpen,
  getDropdownLinks,
  testSearchFunctionality,
  hasSecondaryNavigation,
  getSecondaryNavigationItems,
  verifyPageLoad,
  isElementVisible,
  clickSearchButton,
  MOBILE_THRESHOLD
} from "../../helpers/navigation-helpers";

test.describe("Navigation Flows - E2E Tests", () => {
  
  test.beforeEach(async ({ page }) => {
    await navigateToHomepage(page);
  });

  test.describe("Primary Navigation Structure", () => {
    
    test("should display all primary navigation items", async ({ page }) => {
      // Verify main navigation is visible
      await expect(page.locator('#navigation')).toBeVisible();
      
      // Check each primary navigation item
      for (const navItem of PRIMARY_NAV_ITEMS) {
        await test.step(`Verify ${navItem.title} navigation item`, async () => {
          const element = page.locator(navItem.selector!);
          await expect(element).toBeVisible();
          
          const linkText = await element.locator('a').first().textContent();
          expect(linkText?.trim()).toBe(navItem.title);
        });
      }
    });

    test("should have correct navigation structure and accessibility", async ({ page }) => {
      // Check navigation has proper ARIA labels
      const nav = page.locator('#navigation nav');
      await expect(nav).toHaveAttribute('aria-label', 'Categories');
      
      // Check primary navigation items have proper roles
      // Only the main navigation items 
      // (Products, Solutions, Partners, Careers, Company) 
      // should have role="menuitem"
      for (const navItem of PRIMARY_NAV_ITEMS) {
        const primaryNavItem = page.locator(navItem.selector!);
        await expect(primaryNavItem).toHaveAttribute('role', 'menuitem');
      }
    });

    test("should display Canonical logo and branding", async ({ page }) => {
      // Check logo image
      const logoImg = page.locator('.p-navigation__logo-icon');
      await expect(logoImg).toBeVisible();
      await expect(logoImg).toHaveAttribute('alt', 'Canonical');
      
      // Check logo title
      const logoTitle = page.locator('.p-navigation__logo-title');
      await expect(logoTitle).toBeVisible();
      await expect(logoTitle).toHaveText('Canonical');
    });
  });

  test.describe("Dropdown Navigation Interactions", () => {
    
    PRIMARY_NAV_ITEMS.forEach(navItem => {
      if (navItem.hasDropdown) {
        test(`should open and close ${navItem.title} dropdown on click`, async ({ page }) => {
          // Skip dropdown tests on mobile (uses different interaction pattern)
          if (await isMobileViewport(page)) {
            test.skip();
          }
          
          // Test dropdown opening
          await test.step(`Open ${navItem.title} dropdown`, async () => {
            await clickNavigationItem(page, navItem.selector!);
            
            // Verify dropdown is open
            const isOpen = await isDropdownOpen(page, navItem.selector!.replace('#', '').replace('-nav', ''));
            expect(isOpen).toBe(true);
          });
          
          // Test dropdown closing by clicking elsewhere
          await test.step(`Close ${navItem.title} dropdown`, async () => {
            // Click elsewhere to close dropdown
            await clickNavigationItem(page, navItem.selector!);
            
            const dropdownId = navItem.selector!.replace('#', '').replace('-nav', '');
            await expect(page.locator(`#${dropdownId}-content`)).not.toBeVisible();
            
            // Verify dropdown is closed
            const isOpen = await isDropdownOpen(page, dropdownId);
            expect(isOpen).toBe(false);
          });
        });

        test(`should open ${navItem.title} dropdown on click for mobile`, async ({ page }) => {
          // Set mobile viewport
          await page.setViewportSize({ width: 375, height: 667 });
          await page.reload();
          await acceptCookiePolicy(page);
          
          // Open mobile menu
          await toggleMobileMenuIfNeeded(page);
          
          // Click navigation item
          await clickNavigationItem(page, navItem.selector!);
          
          // Verify dropdown content appears
          const dropdownId = navItem.selector!.replace('#', '').replace('-nav', '');
          const dropdownContent = page.locator(`#${dropdownId}-content`);
          await expect(dropdownContent).toBeVisible();
        });

        test(`should contain valid links in ${navItem.title} dropdown`, async ({ page }) => {
          // Open dropdown
          if (await isMobileViewport(page)) {
            await toggleMobileMenuIfNeeded(page);
          }
          
          await clickNavigationItem(page, navItem.selector!);
          
          // Get dropdown links
          const dropdownId = navItem.selector!.replace('#', '').replace('-nav', '');
          const links = await getDropdownLinks(page, dropdownId + '-nav');
          
          // Verify we have links
          expect(links.length).toBeGreaterThan(0);
          
          // Test first few links to ensure they're functional
          const dropdownContent = page.locator(`#${dropdownId}-content`);
          const linkElements = dropdownContent.locator('a[href]');
          const linkCount = Math.min(await linkElements.count(), 3); // Test first 3 links
          
          for (let i = 0; i < linkCount; i++) {
            const link = linkElements.nth(i);
            const href = await link.getAttribute('href');
            expect(href).toBeTruthy();
            
            // Verify link is not empty or just '#'
            expect(href).not.toBe('#');
            expect(href?.length).toBeGreaterThan(1);
          }
        });
      }
    });
  }); 

  test.describe("Search Functionality", () => {
    test("should open and close search overlay", async ({ page }) => {
      // Click search button
      await clickSearchButton(page);
      
      // Verify search overlay opens
      await expect(page.locator('.p-navigation__search')).toBeVisible();
      await expect(page.locator('#navigation-search')).toBeVisible();
      
      // Close search by clicking overlay
      const searchOverlay = page.locator('.js-search-overlay');
      await searchOverlay.click();
      
      // Verify search closes
      await expect(page.locator('#navigation-search')).not.toBeVisible();
    });

    test("should clear input on reset", async ({ page }) => {
      // Click search button
      await clickSearchButton(page);
      
      // Verify search overlay opens
      await expect(page.locator('.p-navigation__search')).toBeVisible();
      await expect(page.locator('#navigation-search')).toBeVisible();

      // Type search term
      await page.fill('#navigation-search', "test");
      
      // Verify input contains the typed text
      await expect(page.locator('#navigation-search')).toHaveValue("test");
      
      // Click reset button to clear input
      const resetButton = page.locator('.p-search-box__reset');
      await resetButton.click();
      
      // Verify input is empty after reset
      await expect(page.locator('#navigation-search')).toHaveValue("");
    });

    test("should perform search and navigate to results", async ({ page }) => {
      await testSearchFunctionality(page, "ubuntu server");
      
      // Verify we're on search results page
      await expect(page).toHaveURL(/.*\/search.*/);
      
      // Verify search results page loads
      await verifyPageLoad(page);
    });
  });

  test.describe("Secondary Navigation", () => {
    
    test("should display secondary navigation on appropriate pages", async ({ page }) => {
      // Navigate to a page with secondary navigation
      await page.goto('/data');
      
      if (await hasSecondaryNavigation(page)) {
        // Check secondary navigation items
        const secondaryItems = await getSecondaryNavigationItems(page);
        expect(secondaryItems.length).toBeGreaterThan(0);
        
        // Verify secondary navigation has proper classes
        const secondaryNav = page.locator('#secondary-navigation');
        await expect(secondaryNav).toHaveClass(/p-navigation/);
        await expect(secondaryNav).toHaveClass(/is-secondary/);
      }
    });

    test("should navigate between secondary navigation items", async ({ page }) => {
      // Navigate to a page with secondary navigation
      await page.goto('/data');
      
      if (await hasSecondaryNavigation(page)) {
        const secondaryItems = await getSecondaryNavigationItems(page);
        
        if (secondaryItems.length > 1) {
          // Click on second item if available
          const secondaryLinks = page.locator('#secondary-navigation .p-navigation__items a');
          const secondLink = secondaryLinks.nth(1);
          
          if (await secondLink.isVisible()) {
            const href = await secondLink.getAttribute('href');
            await secondLink.click();
            
            if (href && href !== '#') {
              await verifyPageLoad(page);
              
              // Verify we navigated to the correct page
              if (href.startsWith('/')) {
                await expect(page).toHaveURL(new RegExp(href.replace('/', '\\/')));
              }
            }
          }
        }
      }
    });
  });

  test.describe("Cross-linking Between Navigation Sections", () => {
    
    test("should maintain navigation state when navigating between sections", async ({ page }) => {
      // Start from homepage
      await navigateToHomepage(page);
      
      // Navigate through different sections
      const testPaths = ['/data', '/openstack'];
      
      for (const path of testPaths) {
        await test.step(`Navigate to ${path}`, async () => {
          await page.goto(path);
          
          // Verify primary nav is still present
          await expect(page.locator('#navigation')).toBeVisible();
          
          // Verify all primary nav items are still there
          for (const navItem of PRIMARY_NAV_ITEMS) {
            await expect(page.locator(navItem.selector!)).toBeVisible();
          }
          
          await verifyPageLoad(page);
        });
      }
    });

    test("should handle navigation from dropdown links", async ({ page }) => {
      // Open Products dropdown
      await clickNavigationItem(page, '#products-nav');
      
      // Find and click a dropdown link
      const dropdownContent = page.locator('#products-content');
      const firstLink = dropdownContent.locator('a[href^="/"]').first();
      
      if (await firstLink.isVisible()) {
        const href = await firstLink.getAttribute('href');
        await firstLink.click();
        
        if (href) {
          await verifyPageLoad(page, href);
          
          // Verify navigation is still functional on new page
          await expect(page.locator('#navigation')).toBeVisible();
        }
      }
    });
  });

  test.describe("Mobile Navigation Behavior", () => {
    
    test("should display mobile menu toggle on small screens", async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 });
      await page.reload();
      await acceptCookiePolicy(page)
      
      // Verify mobile menu button is visible
      const menuButton = page.locator('.js-menu-button');
      await expect(menuButton).toBeVisible();
    });

    test("should open and close mobile menu", async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 });
      await page.reload();

      await expect(page.locator('#navigation')).not.toHaveClass(/has-menu-open/);
      
      // Open mobile menu
      await toggleMobileMenuIfNeeded(page);

      await expect(page.locator('#navigation')).toHaveClass(/has-menu-open/);
      
      // Close mobile menu
      await toggleMobileMenuIfNeeded(page);

      await expect(page.locator('#navigation')).not.toHaveClass(/has-menu-open/)
    });
  });

  test.describe("Error Handling", () => {
    test("should handle navigation to non-existent pages", async ({ page }) => {
      // Navigate to a non-existent page
      await page.goto('/non-existent-page-12345');
      
      // Should show 404 page but navigation should still be present
      if (await isElementVisible(page, '#navigation')) {
        await expect(page.locator('#navigation')).toBeVisible();
      }
    });
  });
});

test.describe("Responsive Navigation Tests", () => {

  test.beforeEach(async ({ page }) => {
    await navigateToHomepage(page);
  });
  
  VIEWPORTS.forEach(viewport => {
    test(`should work correctly on ${viewport.name} (${viewport.width}x${viewport.height})`, async ({ page }) => {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      
      // Verify navigation is visible
      await expect(page.locator('#navigation')).toBeVisible();
      
      // Test appropriate interactions based on viewport
      if (viewport.width >= MOBILE_THRESHOLD) {
        // Desktop interactions
        await test.step("Test desktop navigation interactions", async () => {
          // Test click on first navigation item
          const firstNavItem = PRIMARY_NAV_ITEMS[0];
          await clickNavigationItem(page, firstNavItem.selector!);
          
          // Verify dropdown appears
          const dropdownId = firstNavItem.selector!.replace('#', '').replace('-nav', '');
          const dropdownContent = page.locator(`#${dropdownId}-content`);
          await expect(dropdownContent).toBeVisible();
        });
      } else {
        // Mobile interactions
        await test.step("Test mobile navigation interactions", async () => {
          // Verify mobile menu button exists
          const menuButton = page.locator('.js-menu-button');
          await expect(menuButton).toBeVisible();
          
          // Test mobile menu toggle
          await toggleMobileMenuIfNeeded(page);
        });
      }
      
      // Test search functionality on all screen sizes
      await test.step("Test search functionality", async () => {
        const searchButton = page.locator('.js-search-button').first();
        if (await searchButton.isVisible()) {
          await searchButton.click();
          await expect(page.locator('#navigation-search')).toBeVisible();
        }
      });
    });
  });
});

test.describe("Navigation Accessibility", () => {

  test.beforeEach(async ({ page }) => {
    await navigateToHomepage(page);
  });
  
  test("should have proper ARIA attributes and keyboard navigation", async ({ page }) => {
    // Check main navigation has proper ARIA
    const mainNav = page.locator('#navigation nav');
    await expect(mainNav).toHaveAttribute('aria-label');
    
    // Check dropdown buttons have proper ARIA attributes
    const dropdownButtons = mainNav.locator('.p-navigation__items[role="menuitem"] .js-dropdown-button');
    const count = await dropdownButtons.count();
    
    for (let i = 0; i < count; i++) {
      const button = dropdownButtons.nth(i);
      await expect(button).toHaveAttribute('aria-controls');
      await expect(button).toHaveAttribute('tabindex', '0');
    }
  });

  test("should support keyboard navigation", async ({ page }) => {
    const firstNavButton = page.locator('.js-dropdown-button').first();
    await firstNavButton.focus();
    await expect(firstNavButton).toBeFocused();
    await page.keyboard.press('Enter');
    const controls = await firstNavButton.getAttribute('aria-controls');
    expect(controls).toBeTruthy();
    const dropdownContent = page.locator(`#${controls}`);
    await expect(dropdownContent).toBeVisible();
  });
});

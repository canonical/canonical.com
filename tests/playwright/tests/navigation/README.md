# Navigation E2E Tests

This directory contains end-to-end tests for the Canonical.com navigation system.

## Test Coverage

### Primary Navigation Tests
- **Structure Validation**: Verifies all primary navigation items (Products, Solutions, Partners, Careers, Company) are present and properly structured
- **Accessibility**: Tests ARIA attributes, keyboard navigation, and screen reader compatibility
- **Branding**: Validates Canonical logo and branding elements

### Dropdown Navigation Tests
- **Click Interactions**: Tests dropdown opening/closing on desktop click
- **Touch Interactions**: Tests dropdown behavior on mobile/touch devices
- **Link Validation**: Verifies all dropdown links are functional and lead to valid pages
- **Content Verification**: Ensures dropdown content matches navigation.yaml structure
- **Closing Behavior**: Verifies dropdown collapses when clicking the same item or outside the navigation
- **ARIA Buttons**: Ensures dropdown buttons have `aria-controls` and `tabindex="0"`

### Search Functionality Tests
- **Search Overlay**: Tests search interface opening/closing
- **Search Execution**: Validates search functionality with various queries
- **Error Handling**: Tests empty search and edge cases

### Secondary Navigation Tests
- **Conditional Display**: Tests secondary navigation appears on appropriate pages
- **Navigation Flow**: Validates navigation between secondary menu items
- **Cross-linking**: Tests integration between primary and secondary navigation

### Responsive Behavior Tests
- **Multiple Viewports**: Tests across 6 different viewport sizes:
  - Desktop Large (1920x1080)
  - Desktop Standard (1366x768)
  - Tablet Landscape (1024x768)
  - Tablet Portrait (768x1024)
  - Mobile (375x667)
  - Mobile Small (320x568)
- **Mobile Menu**: Tests mobile menu toggle and interactions
- **Adaptive Behavior**: Verifies navigation adapts properly to different screen sizes

### Performance and Loading Tests
- **Error Handling**: Tests navigation behavior on slow networks and error pages
- **State Management**: Verifies navigation state is maintained across page transitions

## Test Files

- `navigation-flows.spec.ts`: Main test file containing all navigation test suites
- `../helpers/navigation-helpers.ts`: Helper functions and utilities for navigation testing

## Running the Tests

### Run All Navigation Tests
```bash
npx playwright test --project=navigation
```

### Run Specific Test Suite
```bash
npx playwright test --project=navigation --grep "Primary Navigation"
```

### Run Tests in Headed Mode (with browser UI)
```bash
npx playwright test --project=navigation --headed
```

### Run Tests with Debug Mode
```bash
npx playwright test --project=navigation --debug
```

### Generate Test Report
```bash
npx playwright test --project=navigation --reporter=html
```

## Test Data Sources

The tests are based on the actual navigation configuration files:
- `navigation.yaml`: Primary navigation structure and dropdown content
- `secondary-navigation.yaml`: Secondary navigation definitions for specific pages

## Helper Functions

The navigation tests use specialized helper functions located in `../helpers/navigation-helpers.ts`:

Core data and constants:
- `PRIMARY_NAV_ITEMS`: Canonical primary navigation items and selectors
- `VIEWPORTS`: Common viewport configurations for responsive testing
- `MOBILE_THRESHOLD`: Width used to branch desktop vs. mobile behavior

Navigation helpers:
- `acceptCookiePolicy()`: Handles cookie consent banner
- `navigateToHomepage()`: Navigates to the homepage and prepares clean state
- `isElementVisible()`: Convenience visibility check for selectors
- `isMobileViewport()`: Returns true if current viewport is mobile-sized
- `toggleMobileMenuIfNeeded()`: Toggles the mobile menu when in mobile viewport
- `clickNavigationItem()`: Clicks a primary navigation item
- `isDropdownOpen()`: Checks if a dropdown is currently expanded
- `getDropdownLinks()`: Extracts dropdown link texts (first few links validated for href)
- `clickSearchButton()`: Opens the search overlay via the toolbar button
- `testSearchFunctionality()`: Performs a search and validates navigation
- `hasSecondaryNavigation()` / `getSecondaryNavigationItems()`: Secondary menu helpers
- `verifyPageLoad()`: Validates successful page transitions

## Viewport Testing

The tests include comprehensive responsive testing across multiple device sizes:
- Desktop environments (click-based interactions)
- Tablet environments (mixed touch/mouse interactions)  
- Mobile environments (touch-based interactions, mobile menu)
 
Threshold-based behavior:
- Desktop vs. mobile interactions are determined using `MOBILE_THRESHOLD` (currently `1035` pixels)

## Accessibility Testing

Navigation tests include accessibility validation:
- ARIA attributes and labels
- Primary menu items have `role="menuitem"`; submenu items do not
- Keyboard navigation support
- Focus management
- Screen reader compatibility

## Maintenance

When updating navigation structure:
1. Update `navigation.yaml` or `secondary-navigation.yaml` as needed
2. Run the navigation tests to ensure no regressions
3. Update test expectations if navigation structure changes significantly
4. Add new test cases for any new navigation features

### Debug Tips
- Use `--headed` mode to see browser interactions
- Add `await page.pause()` in tests to inspect page state
- Check network tab for failed requests that might affect navigation
- Verify base URL configuration matches your development environment

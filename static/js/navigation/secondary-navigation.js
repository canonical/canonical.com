import { navigation, secondaryNavigation } from "./elements";

import closeAllNavigationItems from "./main";

function initSecondaryNavigation(secondaryNavigation) {
  /**
   * Add event listener for the secondary nav dropdown
   * (only applicable on mobile view)
   */
  const secondaryNavigationToggle = document.querySelector(
    ".js-secondary-menu-toggle-button"
  );
  secondaryNavigationToggle?.addEventListener(
    "click",
    toggleSecondaryNavigation
  );
}

/**
 * Handle the state of the secondary navigation dropdown
 */
function toggleSecondaryNavigation(e) {
  e.preventDefault();
  const isOpen = secondaryNavigation.classList.contains("has-menu-open");
  if (!isOpen) {
    closeAllNavigationItems();
    openSecondaryNavigation();
  } else {
    closeSecondaryNavigation();
  }
}

/**
 * Reset the state of the secondary navigation
 */
export default function closeSecondaryNavigation() {
  secondaryNavigation?.classList.remove("has-menu-open");
}

/**
 * Open the secondary navigation
 */
function openSecondaryNavigation() {
  secondaryNavigation.classList.add("has-menu-open");
}

initSecondaryNavigation(secondaryNavigation);

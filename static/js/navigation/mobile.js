import { navigation, topLevelNavigationItems } from "./elements";

import setFocusable from "./keyboard-navigation";
import closeAllNavigationItems from "./main";
/**
 * Toggle the state of the menu
 */
export function toggleMenu() {
  const isOpen = navigation.classList.contains("has-menu-open");
  closeAllNavigationItems();
  if (!isOpen) {
    openMenu();
  }
}

/**
 * Open the menu
 */
export function openMenu() {
  navigation.classList.add("has-menu-open");
  setFocusable(topLevelNavigationItems);
}

/**
 * Close the menu
 */
export function closeMenu() {
  navigation.classList.remove("has-menu-open");
}

/**
 * Updates the state of the mobile review to back one level
 * @param {HTMLElement} backButton - the clicked back button
 */
export function goBackOneLevel(backButton) {
  const target = backButton.closest(".p-navigation__dropdown");
  target.setAttribute("aria-hidden", "true");
  backButton.closest(".is-active").classList.remove("is-active");
  backButton.closest(".is-active").classList.remove("is-active");
  setFocusable(target.parentNode.parentNode);
}

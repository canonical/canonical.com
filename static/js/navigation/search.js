import { navigation, secondaryNavigation } from "./elements";

import closeAllNavigationItems from "./main";

/**
 * Handle the state of the search
 */
export function toggleSearch() {
  const isOpen = navigation.classList.contains("has-search-open");

  if (!isOpen) {
    closeAllNavigationItems();
    openSearch();
  } else {
    closeAllNavigationItems();
  }
}

/**
 * Resets the state of the search bar
 */
export function closeSearch() {
  const searchToggle = document.querySelector(".js-search-button");
  searchToggle.removeAttribute("aria-pressed");
  navigation.classList.remove("has-search-open");
  secondaryNavigation?.classList.remove("has-search-open");
}

/**
 * Opens the search.
 * It searchs for the input in the normal nav; if not found, checks
 * the secondary nav, as reduced nav is currently rendered.
 */
function openSearch() {
  const searchToggle = document.querySelector(".js-search-button");
  const searchInput = navigation.querySelector(".p-search-box__input");
  searchToggle.setAttribute("aria-pressed", "true");
  secondaryNavigation?.classList.add("has-search-open");
  navigation.classList.add("has-search-open");
  searchInput.focus();
}

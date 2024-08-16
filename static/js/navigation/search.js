import { navigation, secondaryNavigation } from "./elements";
import { handleSearchKeyboardControls } from "./keyboard-navigation";
import closeAllNavigationItems from "./main";

/**
 * Handle clicks relating to search functionality
 * @param {HTMLElement} element - The element that triggered the event.
 */
export function handleSearch(element) {
  if (element.type === "submit") {
    const form = element.closest("form");
    if (form) {
      form.submit();
    } else {
      console.error("No form found to submit");
    }
  } else if (element.type === "reset") {
    const form = element.closest("form");
    if (form) {
      form.reset();
    } else {
      console.error("No form found to reset");
    }
  } else {
    toggleSearch();
  }
}

/**
 * Toggle the state of the search
 */
function toggleSearch() {
  const isOpen = navigation.classList.contains("has-search-open");
  closeAllNavigationItems();
  if (!isOpen) {
    openSearch();
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
  document.removeEventListener("keydown", handleSearchKeyboardControls);
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
  document.addEventListener("keydown", handleSearchKeyboardControls);
}

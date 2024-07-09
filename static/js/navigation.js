/**
 * Add event delegation handler to navigation container
 */
const navigationContainer = document.querySelector(
  ".p-navigation, .p-navigation--reduced"
);
navigationContainer.addEventListener("click", (e) => {
  e.preventDefault();
  const target = e.target;

  if (target.matches(".js-search-button")) {
    toggleSearch();
  } else if (target.closest("a")) {
    window.location.href = target.href || "/";
  }
});

/**
 * Add event listener for the secondary nav dropdown
 * (only applicable on mobile view)
 */
const secondaryNav = document.querySelector(".p-navigation.is-secondary");
const secondaryNavToggle = document.querySelector(
  ".js-secondary-menu-toggle-button"
);
secondaryNavToggle?.addEventListener("click", toggleSecondaryNavigation);

/**
 * Add event listener to search overlay, to close all on click
 */
const overlay = document.querySelector(".js-search-overlay");
if (overlay) {
  overlay.addEventListener("click", closeAll);
}

/**
 * Handle the state of the secondary navigation dropdown
 */
function toggleSecondaryNavigation(e) {
  e.preventDefault();
  const isOpen = secondaryNav.classList.contains("has-menu-open");
  if (!isOpen) {
    closeAll();
    openSecondaryNavigation();
  } else {
    closeSecondaryNavigation();
  }
}

/**
 * Reset the state of the secondary navigation
 */
function closeSecondaryNavigation() {
  secondaryNav?.classList.remove("has-menu-open");
}

/**
 * Open the secondary navigation
 */
function openSecondaryNavigation() {
  secondaryNav.classList.add("has-menu-open");
}

/**
 * Handle the state of the search
 */
function toggleSearch() {
  const isOpen = navigationContainer.classList.contains("has-search-open");

  if (!isOpen) {
    closeAll();
    openSearch();
  } else {
    closeAll();
  }
}

/**
 * Resets the state of the search bar
 */
function closeSearch() {
  const searchToggle = document.querySelector(".js-search-button");
  searchToggle.removeAttribute("aria-pressed");
  navigationContainer.classList.remove("has-search-open");
  secondaryNav?.classList.remove("has-search-open");
}

/**
 * Opens the search.
 * It searchs for the input in the normal nav; if not found, checks
 * the secondary nav, as reduced nav is currently rendered.
 */
function openSearch() {
  const searchToggle = document.querySelector(".js-search-button");
  const searchInput = navigationContainer.querySelector(".p-search-box__input");
  searchToggle.setAttribute("aria-pressed", "true");
  secondaryNav?.classList.add("has-search-open");
  navigationContainer.classList.add("has-search-open");
  searchInput.focus();
}

/**
 * Reset the state of everything
 */
function closeAll() {
  closeSearch();
  closeSecondaryNavigation();
}

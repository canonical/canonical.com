import throttle from "../utils/throttle";

import {
  navigation,
  secondaryNavigation,
  toggles,
  topLevelNavigationItems,
} from "./elements";

import { closeSearch, handleSearch } from "./search";
import closeSecondaryNavigation from "./secondary-navigation";
import {
  setFocusable,
  handleDesktopKeyboardEvents,
} from "./keyboard-navigation";
import { toggleMenu, closeMenu, goBackOneLevel } from "./mobile";
import populateCareersRoles from "./careers/populate-careers-roles";
import initGATracking from "./ga-tracking";

const ANIMATION_SNAP_DURATION = 100;

/**
 * Add event delegation handler to navigation container.
 * This controls any items within the navigation that are clicked.
 */
navigation.addEventListener("click", (e) => {
  e.preventDefault();
  const target = e.target.closest("a, button");
  if (!target) {
    return;
  } else if (target.matches(".js-dropdown-button")) {
    toggleDropdown(target);
  } else if (target.matches(".js-search-button")) {
    handleSearch(target);
  } else if (target.matches(".js-menu-button")) {
    toggleMenu();
  } else if (target.matches(".js-back-button")) {
    goBackOneLevel(target);
  } else if (target.closest("a")) {
    window.location.href = target.closest("a").href || "/";
  }
});

/**
 * Add event listener to search overlay, to close all on click
 */
const overlay = document.querySelector(".js-search-overlay");
if (overlay) {
  overlay.addEventListener("click", closeAllNavigationItems);
}

/**
 * Add event listener to document, to close all navigation items if user
 * clicks outside the navigation
 */
document.addEventListener("click", function (event) {
  const target = event.target;
  if (target.closest) {
    if (
      !target.closest(
        ".p-navigation--sliding, .p-navigation--reduced, .p-navigation.is-secondary"
      )
    ) {
      closeAllNavigationItems();
    }
  }
});

/**
 * Handles when any toggle is clicked by reseting the other toggles and
 * managing whether the animation should run
 * @param {HTMLElement} toggle - The clicked toggle
 */
function toggleDropdown(toggle) {
  const target = document.getElementById(toggle.getAttribute("aria-controls"));
  if (target) {
    // check if the toggled dropdown is child of another dropdown
    const isNested = target.parentNode.closest(".p-navigation__dropdown");
    if (!isNested) {
      resetToggles(target);
    }
    if (target.getAttribute("aria-hidden") === "true") {
      // only animate the dropdown if menu is not open, otherwise just switch the visible one
      expandDropdown(
        toggle,
        target,
        !navigation.classList.contains("has-menu-open")
      );
      navigation.classList.add("has-menu-open");
      navigation.addEventListener("keydown", handleDesktopKeyboardEvents);
    } else {
      collapseDropdown(toggle, target, true);
      setFocusable();
      navigation.classList.remove("has-menu-open");
      navigation.removeEventListener("keydown", handleDesktopKeyboardEvents);
    }
  }
}

/**
 * Resets all toggles to their base state, unless an exception is passed
 * then this toggle is ignored
 * @param {HTMLElement} exception - The toggle to ignore
 */
const resetToggles = (exception) => {
  toggles.forEach(function (toggle) {
    const target = document.getElementById(
      toggle.getAttribute("aria-controls")
    );
    if (!target || target === exception) {
      return;
    }
    collapseDropdown(toggle, target);
  });
};

/**
 * Closing a specific dropdown and updates the state, effects both mobile
 * and desktop
 * @param {HTMLElement} dropdownToggleButton - The toggle clicked
 * @param {HTMLElement} targetDropdown - The effected dropdown list
 * @param {Bool} animated - Whether to anitmate it
 */
const collapseDropdown = (
  dropdownToggleButton,
  targetDropdown,
  animated = false
) => {
  const closeHandler = () => {
    dropdownToggleButton.parentNode.classList.remove("is-active");
    dropdownToggleButton.parentNode.parentNode.classList.remove("is-active");
    targetDropdown.setAttribute("aria-hidden", "true");
  };

  targetDropdown.classList.add("is-collapsed");
  if (animated) {
    setTimeout(closeHandler, ANIMATION_SNAP_DURATION);
  } else {
    closeHandler();
  }
};

/**
 * Open a specific dropdown and updates the state, effects both mobile
 * and desktop
 * @param {HTMLElement} dropdownToggleButton - The toggle clicked
 * @param {HTMLElement} targetDropdown - The effected dropdown list
 * @param {Bool} animated - Whether to anitmate it
 */
const expandDropdown = (
  dropdownToggleButton,
  targetDropdown,
  animated = false
) => {
  dropdownToggleButton.closest(".js-dropdown-list").classList.add("is-active");
  targetDropdown.setAttribute("aria-hidden", "false");
  if (targetDropdown.classList.contains("js-dropdown-list")) {
    targetDropdown.classList.add("is-active");
  } else {
    dropdownToggleButton.parentNode.classList.add("is-active");
  }
  if (animated) {
    // trigger the CSS transition
    requestAnimationFrame(() => {
      targetDropdown.classList.remove("is-collapsed");
    });
  } else {
    // make it appear immediately
    targetDropdown.classList.remove("is-collapsed");
  }

  setFocusable(targetDropdown);
};

navigation.querySelectorAll(".js-navigation-tab").forEach((tab) => {
  tab.addEventListener("click", toggleSection);
});
// Attaches to tab items in desktop dropdown and updates them,
// also applies the same update to the mobile dropdown.
// Is attached via HTML onclick attribute.
function toggleSection(e) {
  e.preventDefault();
  e.stopPropagation();
  const targetId = e.target.getAttribute("aria-controls");
  const el = document.querySelector(`.js-dropdown-window #${targetId}`);
  const currTabWindow = e.target.closest(".js-dropdown-window");
  const tabLinks = currTabWindow.querySelectorAll(".p-side-navigation__link");
  tabLinks.forEach((tabLink) => {
    const tabId = tabLink.getAttribute("aria-controls");
    const tabWindow = currTabWindow.querySelector(`#${tabId}`);
    if (tabId === targetId) {
      el.removeAttribute("hidden");
      tabLink.setAttribute("aria-selected", true);
      tabLink.classList.add("is-active");
    } else {
      tabWindow.setAttribute("hidden", true);
      tabLink.setAttribute("aria-selected", false);
      tabLink.classList.remove("is-active");
    }
  });
}

/**
 * Reset the state of everything in the navigation
 * @param {Object} options - Options for the function
 * @param {String} options.exception - The navigation item to ignore
 */
function closeAllNavigationItems({ exception } = {}) {
  // prettier-ignore
  const actions = {
    "search": closeSearch,
    "secondary-navigation": closeSecondaryNavigation,
    "main-toggles": resetToggles,
    "menu": closeMenu,
    "set-focus": setFocusable,
  };

  for (const key in actions) {
    if (key !== exception) {
      actions[key]();
    }
  }
}

// Hide navigation when screen is horizontally resized
let previousWidth = window.innerWidth;
window.addEventListener(
  "resize",
  throttle(function () {
    const currentWidth = window.innerWidth;
    if (currentWidth !== previousWidth) {
      closeAllNavigationItems();
      previousWidth = currentWidth;
    }
  }, 10)
);

// Update careers dropdown with latest avaiable roles
populateCareersRoles();

// Init GA tracking
initGATracking();

export default closeAllNavigationItems;

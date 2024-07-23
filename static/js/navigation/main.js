import { navigation, secondaryNavigation, toggles } from "./elements";

import { closeSearch, toggleSearch } from "./search";
import closeSecondaryNavigation from "./secondary-navigation";
import setFocusable from "./keyboard-navigation";
import { toggleMenu, closeMenu, goBackOneLevel } from "./mobile";

const ANIMATION_SNAP_DURATION = 100;

/**
 * Add event delegation handler to navigation container.
 * This controls any items within the navigation that are clicked.
 */
navigation.addEventListener("click", (e) => {
  e.preventDefault();
  const target = e.target;
  if (target.matches(".js-dropdown-button")) {
    handleToggle(target);
  } else if (target.matches(".js-search-button")) {
    toggleSearch();
  } else if (target.matches(".js-menu-button")) {
    toggleMenu();
  } else if (target.matches(".js-back-button")) {
    goBackOneLevel(e.target);
  } else if (target.closest("a")) {
    window.location.href = target.href || "/";
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
function handleToggle(toggle) {
  const target = document.getElementById(toggle.getAttribute("aria-controls"));
  if (target) {
    // check if the toggled dropdown is child of another dropdown
    const isNested = !!target.parentNode.closest(".p-navigation__dropdown");
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
    } else {
      collapseDropdown(toggle, target, true);
      navigation.classList.remove("has-menu-open");
    }
  }
}

/**
 * Resets all toggles to there base state, unless an exception is passed
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
    targetDropdown.setAttribute("aria-hidden", "true");
    dropdownToggleButton.parentNode.classList.remove("is-active");
    dropdownToggleButton.parentNode.parentNode.classList.remove("is-active");
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
  dropdownToggleButton.parentNode.classList.add("is-active");
  dropdownToggleButton.parentNode.parentNode.classList.add("is-active");
  targetDropdown.setAttribute("aria-hidden", "false");
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
  };

  for (const key in actions) {
    if (key !== exception) {
      actions[key]();
    }
  }
}

// throttle util (for window resize event)
var throttle = function (fn, delay) {
  var timer = null;
  return function () {
    var context = this,
      args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function () {
      fn.apply(context, args);
    }, delay);
  };
};

// hide side navigation drawer when screen is resized
window.addEventListener("resize", throttle(closeAllNavigationItems, 10));

export default closeAllNavigationItems;

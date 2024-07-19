import { navigation, secondaryNavigation } from "./elements";

import { closeSearch, toggleSearch } from "./search";
import closeSecondaryNavigation from "./secondary-navigation";

const dropdowns = document.querySelectorAll("ul.p-navigation__dropdown");
const lists = [...dropdowns];
const mainList = dropdowns[0]?.parentNode?.parentNode;
if (mainList) {
  lists.push(mainList);
}
const mainToggles = document.querySelectorAll(
  ".p-navigation__nav .p-navigation__link[aria-controls]:not(.js-back)"
);

/**
 * Add event delegation handler to navigation container.
 * This controls any items within the navigation that are clicked.
 */
navigation.addEventListener("click", (e) => {
  e.preventDefault();
  const target = e.target;

  if (target.parentNode.getAttribute("role") === "menuitem") {
    handleMainToggles(target);
  } else if (target.matches(".js-search-button")) {
    toggleSearch();
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
 * Add event listener to document, to reset dropdown toggle if you click
 * outide the navigation
 */
document.addEventListener("click", function (e) {
  const target = e.target;
  if (target.closest) {
    if (!target.closest(".p-navigation--sliding, .p-navigation--reduced")) {
      resetMainToggles(e);
      navigation.classList.remove("has-menu-open");
    }
  }
});

/**
 * Resets top level toggles back to their original state
 * @param {HTMLElement} excludedToggle - A toggle to ignore
 */
function resetMainToggles(excludedToggle) {
  mainToggles.forEach(function (toggle) {
    const target = document.getElementById(
      toggle.getAttribute("aria-controls")
    );
    if (!target || target === excludedToggle) {
      return;
    }
    target.setAttribute("aria-hidden", "true");
    target.classList.add("is-collapsed");
    toggle.parentNode.classList.remove("is-active");
    toggle.parentNode.parentNode.classList.remove("is-active");
  });
}

/**
 * A function that handles toggle clicks by setting their state and
 * managing animations
 * @param {HTMLElement} toggle - The toggle clicked
 */
function handleMainToggles(toggle) {
  const target = document.getElementById(toggle.getAttribute("aria-controls"));

  const isNested = !target.closest(".p-navigation__dropdown");
  if (!isNested) {
    resetMainToggles(target);
  }

  const toggleIsActive = target.getAttribute("aria-hidden") === "false";
  if (!toggleIsActive) {
    toggle.parentNode.classList.add("is-active");
    toggle.parentNode.parentNode.classList.add("is-active");
    target.setAttribute("aria-hidden", "false");

    const menuIsOpen = navigation.classList.contains("has-menu-open");
    if (!menuIsOpen) {
      // trigger the CSS transition
      requestAnimationFrame(() => {
        target.classList.remove("is-collapsed");
      });
    } else {
      // make it appear immediately
      target.classList.remove("is-collapsed");
    }
    navigation.classList.add("has-menu-open");
    setFocusable(target);
  } else if (toggleIsActive) {
    target.classList.add("is-collapsed");
    setTimeout(() => {
      target.setAttribute("aria-hidden", "true");
      toggle.parentNode.classList.remove("is-active");
      toggle.parentNode.parentNode.classList.remove("is-active");
      navigation.classList.remove("has-menu-open");
    }, 100);
  }
}

/**
 * Sets tabindex for appropriate navigation items to allow keyboard navigation
 * @param {HTMLElement} target - the click target
 */
function setFocusable(target) {
  lists.forEach(function (list) {
    const elements = list.querySelectorAll("ul > li > a, ul > li > button");
    elements.forEach(function (element) {
      element.setAttribute("tabindex", "-1");
    });
  });
  if (target) {
    target.querySelectorAll("li").forEach(function (element) {
      if (element.parentNode === target) {
        element.children[0].setAttribute("tabindex", "0");
      }
    });
  }
}

/**
 * Reset the state of everything in the navigation
 */
function closeAllNavigationItems() {
  closeSearch();
  closeSecondaryNavigation();
  resetMainToggles();
  navigation.classList.remove("has-menu-open");
}

export default closeAllNavigationItems;

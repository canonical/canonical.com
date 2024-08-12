import { lists } from "./elements";
import closeAllNavigationItems from "./main";

/**
 * Sets tabindex for appropriate navigation items to allow keyboard navigation
 * @param {HTMLElement} target - The ul to target
 */
export function setFocusable(target) {
  const isList = target.classList.contains("js-dropdown-list");
  if (!isList) {
    target = target.querySelector(".js-dropdown-list");
  }

  lists.forEach(function (list) {
    const elements = list.querySelectorAll("ul > li .js-focus-target");
    elements.forEach(function (element) {
      element.setAttribute("tabindex", "-1");
    });
  });
  if (target) {
    target.querySelectorAll("li").forEach(function (element) {
      if (element.parentNode === target) {
        element
          .querySelector(".js-focus-target")
          ?.setAttribute("tabindex", "0");
      }
    });
  }
}

/**
 * Delegation handler for keybaord navigaton in the mobile view of the
 * navigation.
 * @param {Event} e
 */
export function handleMobileKeyboardEvents(e) {
  if (e.key === "Escape") {
    handleEscapeKey(e);
  } else if (e.key === "Tab") {
    handleMobileTabKey(e);
  }
}

/**
 * Handle tab key when mobile navigation is open. If tab key is pressed on
 * last item of a list, focus the first item.
 * @param {Event} e
 */
function handleMobileTabKey(e) {
  const currentItem = document.activeElement;
  const parentList = currentItem.closest(".js-dropdown-list");
  if (parentList) {
    const siblingListItems = parentList.querySelectorAll(
      ":scope > li:has(.js-focus-target)"
    );
    const lastFocusableItem =
      siblingListItems[siblingListItems.length - 1].querySelector(
        ".js-focus-target"
      );
    const isLastItem =
      siblingListItems[siblingListItems.length - 1] === currentItem;
    if (lastFocusableItem === currentItem) {
      const firstFocusableItem =
        siblingListItems[0].querySelector(".js-focus-target");
      e.preventDefault();
      firstFocusableItem.focus();
    }
  }
}

/**
 * Handles escape key when mobile navigation is open. Closes all navigations.
 * @param {Event} e
 */
function handleEscapeKey(e) {
  closeAllNavigationItems();
}

/**
 * Handles escape key presses when search is open.
 * @param {Event} e
 */
export function handleSearchKeyboardControls(e) {
  if (e.key === "Escape") {
    handleEscapeKey();
  }
}

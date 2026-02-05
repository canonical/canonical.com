import { lists, topLevelNavigationItems } from "./elements";
import closeAllNavigationItems from "./main";

/**
 * Sets tabindex for appropriate navigation items to allow keyboard navigation
 * @param {HTMLElement} target - The ul to target
 */
export function setFocusable(target) {
  if (!target) {
    target = topLevelNavigationItems;
  }
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
 * Delegation handler for keybaord navigaton in the DESKTOP view of the
 * navigation.
 * @param {KeyboardEvent} e
 */
export function handleDesktopKeyboardEvents(e) {
  if (e.key === "Escape") {
    returnFocusToMenuItems(e);
  } else if (e.shiftKey && e.key === "Tab") {
    handleDesktopShiftTabKey(e);
  } else if (e.key === "Tab") {
    handleDesktopTabKey(e);
  } else if (e.key === "Enter") {
    handleDesktopEnterkey(e);
  }
}

/**
 * Handles Shift + Tab key on DESKTOP.
 * @param {KeyboardEvent} e
 */
function handleDesktopShiftTabKey(e) {
  const currentItem = document.activeElement;
  const currentList = getContainingDropdown(currentItem);
  const firstItem = isFirstItem(currentList, currentItem);
  if (firstItem) {
    returnFocusToMenuItems(e);
  }
}

/**
 * Handle tab key when DESKTOP navigation is open.
 * @param {KeyboardEvent} e
 */
function handleDesktopTabKey(e) {
  const currentItem = document.activeElement;
  const currentList = getContainingDropdown(currentItem);
  const lastItem = isLastItem(currentList, currentItem);
  const tabPanel = isInTabPanel(currentList);
  if (lastItem && !tabPanel) {
    returnFocusToMenuItems(e);
  }
}

/**
 * Handle Enter key presses in the desktop navigation. If Enter is clicked
 * on a table panel item, it will focus the first item.
 * @param {KeyboardEvent} e
 */
function handleDesktopEnterkey(e) {
  const currentList = getContainingDropdown(e.target);
  const tabPanel = isInTabPanel(currentList);
  if (tabPanel) {
    const targetId = (e.target).getAttribute("aria-controls");
    const targetPanel = document.querySelector(
      `.js-dropdown-window #${targetId}`
    );
    targetPanel.querySelector("a").focus();
  }
}

/**
 * Closes dropdown and returns focus to the closed dropdowns button.
 */
function returnFocusToMenuItems(e) {
  e.preventDefault();
  /** @type {HTMLElement} */
  const currentActiveDropdown =
    topLevelNavigationItems.querySelector(".is-active > a");
  currentActiveDropdown?.focus();
  closeAllNavigationItems();
}

/**
 * Checks if the current list is the tab panel
 * @param {HTMLElement} list - The list we want to check
 */
function isInTabPanel(list) {
  if (list) {
    return list.classList.contains("js-tabs");
  }
}

/**
 * Returns the containing list the current focus target is in.
 * @param {HTMLElement} target - The event target
 * @returns {HTMLElement}
 */
function getContainingDropdown(target) {
  return (
    target.closest(".js-tabs") ||
    target.closest(".js-content-panel") ||
    target.closest(".js-dropdown-window")
  );
}

/**
 * Delegation handler for keybaord navigaton in the MOBILE view of the
 * navigation.
 * @param {KeyboardEvent} e
 */
export function handleMobileKeyboardEvents(e) {
  if (e.key === "Escape") {
    handleEscapeKey(e);
  } else if (e.key === "Tab") {
    handleMobileTabKey(e);
  }
}

/**
 * Handle tab key when MOBILE navigation is open. If tab key is pressed on
 * last item of a list, focus the first item.
 * @param {KeyboardEvent} e
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
      /** @type {HTMLElement} */
      const firstFocusableItem =
        siblingListItems[0].querySelector(".js-focus-target");
      e.preventDefault();
      firstFocusableItem.focus();
    }
  }
}

/**
 * Handles escape key when ANY navigation is open. Closes all navigations.
 * @param {Event} e
 */
function handleEscapeKey(e) {
  closeAllNavigationItems();
}

/**
 * Handles escape key presses when search is open.
 * @param {KeyboardEvent} e
 */
export function handleSearchKeyboardControls(e) {
  if (e.key === "Escape") {
    handleEscapeKey(e);
  }
}

/**
 * Check if the item losing focus is the last item in a given list.
 * @param {HTMLElement} list - The list we want to check
 * @param {HTMLElement} currentItem - the item we want to compare against the list
 */
function isLastItem(list, currentItem) {
  if (list) {
    const siblingListItems = list.querySelectorAll("a");
    return siblingListItems[siblingListItems.length - 1] === currentItem;
  }
}

/**
 * Check if the item losing focus is the first item in a given list.
 * @param {HTMLElement} list - The list we want to check
 * @param {HTMLElement} currentItem - the item we want to compare against the list
 */
function isFirstItem(list, currentItem) {
  if (list) {
    const firstListitem = list.querySelector("a");
    return firstListitem === currentItem;
  }
}

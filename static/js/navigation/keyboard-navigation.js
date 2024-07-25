import { lists } from "./elements";

/**
 * Sets tabindex for appropriate navigation items to allow keyboard navigation
 * @param {HTMLElement} target - The ul to target
 */
export default function setFocusable(target) {
  const isList = target.classList.contains("js-dropdown-list");
  if (!isList) {
    target = target.querySelector(".js-dropdown-list");
  }

  lists.forEach(function (list) {
    const elements = list.querySelectorAll(
      "ul > li > a, ul > li > button, ul > li > h2"
    );
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

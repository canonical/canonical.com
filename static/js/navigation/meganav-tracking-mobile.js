import { navigation, topLevelNavigationItems } from "./elements";
import { push, segmentString, textify, getLinkTitle } from "./meganav-tracking";

function buildBaseValuesMobile() {
  return { event: "meganav click mobile" };
}

function getTopbarInfoMobile(contextEl) {
  const list = topLevelNavigationItems;
  if (!list) return null;
  const items = Array.from(
    list.querySelectorAll(
      ".p-navigation__item--dropdown-toggle > .js-dropdown-button"
    )
  );

  // Map mobile dropdown container back to its controlling topbar button
  const dropdownContainer = contextEl?.closest?.(".p-navigation__dropdown");
  if (dropdownContainer && dropdownContainer.id) {
    const control = list.querySelector(
      `.js-dropdown-button[aria-controls="${dropdownContainer.id}"]`
    );
    if (control) {
      const idx = items.indexOf(control) + 1;
      return { index: idx, label: textify(control) };
    }
  }

  // Fallbacks: if the element itself is a topbar toggle, or use active one
  const selfTopbar = contextEl.matches?.(
    ".js-dropdown-button[data-level='0']"
  )
    ? contextEl
    : null;
  const active =
    list.querySelector(".is-active > .js-dropdown-button") || selfTopbar;
  if (active) {
    const idx = items.indexOf(active) + 1;
    return { index: idx, label: textify(active) };
  }
  return null;
}

function getMobileGroupInfo(el) {
  const container = el.closest(".p-navigation__dropdown-content--sliding");
  if (!container) return null;

  // Case 1: inside nested nav_section list
  const nestedList = el.closest("ul.p-navigation__dropdown.js-dropdown-list");
  if (nestedList && nestedList.id) {
    const togglers = Array.from(
      container.querySelectorAll(
        ".p-navigation__item--dropdown-toggle > a.js-dropdown-button[data-level='1']"
      )
    );
    const toggler = togglers.find(
      (btn) => btn.getAttribute("aria-controls") === nestedList.id
    );
    if (togglers.length && toggler) {
      const idx = togglers.indexOf(toggler) + 1;
      return { index: idx, label: textify(toggler) };
    }
  }

  // Case 2: general heading groups within the main list
  const list = container.querySelector("ul.js-dropdown-list");
  if (!list) return null;
  const headings = Array.from(
    list.querySelectorAll("li.p-navigation--list-heading")
  );
  let headingEl = null;
  const li = el.closest("li");
  if (li) {
    let prev = li.previousElementSibling;
    while (prev) {
      if (prev.matches("li.p-navigation--list-heading")) {
        headingEl = prev;
        break;
      }
      prev = prev.previousElementSibling;
    }
  }
  if (headingEl) {
    const idx = headings.indexOf(headingEl) + 1;
    const labelEl =
      headingEl.querySelector(".p-navigation__dropdown-item") || headingEl;
    return { index: idx, label: textify(labelEl) };
  }
  return null;
}

function getMobileItemInfo(a) {
  const li = a.closest("li");
  if (li && li.parentElement) {
    const siblings = Array.from(li.parentElement.children).filter(
      (el) => !el.matches(".p-navigation__item--dropdown-close")
    );
    const idx = siblings.indexOf(li) + 1;
    return { index: idx, label: getLinkTitle(a) };
  }
  return { index: 0, label: getLinkTitle(a) };
}

function handleMobileMenuButtonClick() {
  const values = buildBaseValuesMobile();
  values.mega_nav_area = "menu";
  values.click_label = "menu";
  values.click_action = navigation.classList.contains("has-menu-open")
    ? "close"
    : "open";
  push(values);
}

function handleMobileBackClick(btn) {
  const level = parseInt(btn.getAttribute("data-level") || "1", 10);
  const values = buildBaseValuesMobile();
  values.mega_nav_area = `level-${level}`;
  values.click_label = "back";
  push(values);
}

function handleMobileLevel1ToggleClick(a) {
  const topbar = getTopbarInfoMobile(a);
  if (!topbar) return;
  const values = buildBaseValuesMobile();
  values.mega_nav_area = "level-1";
  values.click_label = segmentString(topbar.index, topbar.label);
  values.mega_nav_path = values.click_label;
  push(values);
}

function handleMobileNavSectionToggleClick(a) {
  const topbar = getTopbarInfoMobile(a);
  if (!topbar) return;
  const container = a.closest(".p-navigation__dropdown-content--sliding");
  const togglers = Array.from(
    container.querySelectorAll(
      ".p-navigation__item--dropdown-toggle > a.js-dropdown-button[data-level='1']"
    )
  );
  const idx = togglers.indexOf(a) + 1;
  const values = buildBaseValuesMobile();
  values.mega_nav_area = "level-2";
  const groupSeg = segmentString(idx, textify(a));
  const topbarSeg = segmentString(topbar.index, topbar.label);
  values.click_label = groupSeg;
  values.mega_nav_path = `${topbarSeg} | ${groupSeg}`;
  push(values);
}

function handleMobileExternalLinkClick(a) {
  const topbar = getTopbarInfoMobile(a);
  if (!topbar) return;
  const values = buildBaseValuesMobile();
  values.mega_nav_area = "level-3";

  const item = getMobileItemInfo(a);
  const itemSeg = segmentString(item.index, item.label);
  const topbarSeg = segmentString(topbar.index, topbar.label);
  const group = getMobileGroupInfo(a);
  const parts = [topbarSeg];
  if (group && group.label) parts.push(segmentString(group.index, group.label));
  parts.push(itemSeg);
  values.click_label = itemSeg;
  values.mega_nav_path = parts.join(" | ");

  if (a.href) {
    values.click_from = window.location.origin;
    values.click_to = a.href;
  }

  push(values);
}

export default function initMeganavTrackingMobile() {
  const root = navigation;
  if (!root) return;

  // Mobile: menu button open/close
  root.querySelectorAll(".js-menu-button").forEach((btn) => {
    btn.addEventListener("click", () => handleMobileMenuButtonClick());
  });

  // Mobile: back button clicks
  root
    .querySelectorAll(
      ".p-navigation__dropdown-content--sliding .js-back-button"
    )
    .forEach((btn) => {
      btn.addEventListener("click", () => handleMobileBackClick(btn));
    });

  // Mobile: top-level section toggles (Products, Solutions, etc.)
  root
    .querySelectorAll(
      ".js-dropdown-button[data-level='0']"
    )
    .forEach((a) => {
      a.addEventListener("click", () => handleMobileLevel1ToggleClick(a));
    });

  // Mobile: nav_section toggles inside a top-level section
  root
    .querySelectorAll(
      ".p-navigation__dropdown-content--sliding .p-navigation__item--dropdown-toggle > a.js-dropdown-button[data-level='1']"
    )
    .forEach((a) => {
      a.addEventListener("click", () => handleMobileNavSectionToggleClick(a));
    });

  // Mobile: external navigation clicks (links leading out of the menu)
  root
    .querySelectorAll(
      ".p-navigation__dropdown-content--sliding a"
    )
    .forEach((a) => {
      // Ignore menu-internal controls
      if (
        a.classList.contains("js-back-button") ||
        a.classList.contains("js-dropdown-button") ||
        (a.getAttribute("href") || "").startsWith("#")
      ) {
        return;
      }
      a.addEventListener("click", () => handleMobileExternalLinkClick(a));
    });
}
import { navigation, topLevelNavigationItems } from "./elements";
import {
  ensureDataLayerInitialized,
  getText,
  getElementTitle,
  formatSegment,
  joinSegments,
  pushToDataLayer
} from "./utils";

// ---------------------------------------------
// DOM Lookups & Segment Builders (Mobile)
// ---------------------------------------------
function findMobileDropdownContainer(contextEl) {
  return contextEl?.closest?.(".p-navigation__dropdown") || null;
}

function getTopbarSegmentMobile(contextEl) {
  const listEl = topLevelNavigationItems;
  if (!listEl) return null;

  const topbarButtons = Array.from(
    listEl.querySelectorAll(
      ".p-navigation__item--dropdown-toggle > .js-dropdown-button"
    )
  );

  // Map mobile dropdown container back to its controlling topbar button
  const dropdownContainer = findMobileDropdownContainer(contextEl);
  if (dropdownContainer && dropdownContainer.id) {
    const controlButton = listEl.querySelector(
      `.js-dropdown-button[aria-controls="${dropdownContainer.id}"]`
    );
    if (controlButton) {
      const index = topbarButtons.indexOf(controlButton) + 1;
      return { index, label: getText(controlButton) };
    }
  }

  // Fallbacks: if the element itself is a topbar toggle, or use active one
  const selfTopbar = contextEl.matches?.(".js-dropdown-button[data-level='0']")
    ? contextEl
    : null;
  const activeButton =
    listEl.querySelector(".is-active > .js-dropdown-button") || selfTopbar;
  if (activeButton) {
    const index = topbarButtons.indexOf(activeButton) + 1;
    return { index, label: getText(activeButton) };
  }
  return null;
}

function getMobileGroupSegment(el) {
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
      const index = togglers.indexOf(toggler) + 1;
      return { index, label: getText(toggler) };
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
    const index = headings.indexOf(headingEl) + 1;
    const labelEl =
      headingEl.querySelector(".p-navigation__dropdown-item") || headingEl;
    return { index, label: getText(labelEl) };
  }
  return null;
}

function getMobileItemSegment(a) {
  const li = a.closest("li");
  if (li && li.parentElement) {
    const siblings = Array.from(li.parentElement.children).filter(
      (el) => !el.matches(".p-navigation__item--dropdown-close")
    );
    const index = siblings.indexOf(li) + 1;
    return { index, label: getElementTitle(a) };
  }
  return { index: 0, label: getElementTitle(a) };
}

function buildBaseEventMobile() {
  return { event: "meganav click mobile" };
}

function buildClickEventMobile({ area, pathSegments, clickLabel, href }) {
  const values = buildBaseEventMobile();
  values.mega_nav_area = area;
  values.click_label = clickLabel;
  values.mega_nav_path = joinSegments(pathSegments);

  if (href) {
    values.click_from = window.location.origin;
    values.click_to = href;
  }
  return values;
}

// ---------------------------------------------
// Tracking Handlers (Mobile)
// ---------------------------------------------
function trackMobileMenuButtonClick() {
  const values = buildBaseEventMobile();
  values.mega_nav_area = "menu";
  values.click_label = "menu";
  values.click_action = navigation.classList.contains("has-menu-open")
    ? "close"
    : "open";
  pushToDataLayer(values);
}

function trackMobileBackClick(btn) {
  const level = parseInt(btn.getAttribute("data-level") || "1", 10);
  const values = buildBaseEventMobile();
  values.mega_nav_area = `level-${level}`;
  values.click_label = "back";
  pushToDataLayer(values);
}

function trackMobileLevel1ToggleClick(a) {
  const topbar = getTopbarSegmentMobile(a);
  if (!topbar) return;

  const topbarSeg = formatSegment(topbar.index, topbar.label);
  const values = buildClickEventMobile({
    area: "level-1",
    pathSegments: [topbarSeg],
    clickLabel: topbarSeg,
    href: null,
  });

  pushToDataLayer(values);
}

function trackMobileNavSectionToggleClick(a) {
  const topbar = getTopbarSegmentMobile(a);
  if (!topbar) return;

  const container = a.closest(".p-navigation__dropdown-content--sliding");
  const togglers = Array.from(
    container.querySelectorAll(
      ".p-navigation__item--dropdown-toggle > a.js-dropdown-button[data-level='1']"
    )
  );
  const index = togglers.indexOf(a) + 1;
  const groupSeg = formatSegment(index, getText(a));
  const topbarSeg = formatSegment(topbar.index, topbar.label);

  const values = buildClickEventMobile({
    area: "level-2",
    pathSegments: [topbarSeg, groupSeg],
    clickLabel: groupSeg,
    href: null,
  });

  pushToDataLayer(values);
}

function trackMobileExternalLinkClick(a) {
  const topbar = getTopbarSegmentMobile(a);
  if (!topbar) return;

  const item = getMobileItemSegment(a);
  const itemSeg = formatSegment(item.index, item.label);
  const topbarSeg = formatSegment(topbar.index, topbar.label);
  const group = getMobileGroupSegment(a);

  const pathSegments = [topbarSeg];
  if (group && group.label && group.index > 0) pathSegments.push(formatSegment(group.index, group.label));
  pathSegments.push(itemSeg);

  const values = buildClickEventMobile({
    area: "level-3",
    pathSegments,
    clickLabel: itemSeg,
    href: a.href || null,
  });

  pushToDataLayer(values);
}

// Listener tracking for cleanup when switching breakpoints
const mobileListeners = [];
function addMobileListener(el, type, handler, options) {
  el.addEventListener(type, handler, options);
  mobileListeners.push({ el, type, handler, options });
}
export function destroyMeganavTrackingMobile() {
  mobileListeners.forEach(({ el, type, handler, options }) => {
    el.removeEventListener(type, handler, options);
  });
  mobileListeners.length = 0;
}
export default function initMeganavTrackingMobile() {
  const root = navigation;
  if (!root) return;

  // Mobile: menu button open/close
  root.querySelectorAll(".js-menu-button").forEach((btn) => {
    addMobileListener(btn, "click", () => trackMobileMenuButtonClick());
  });

  // Mobile: back button clicks
  root
    .querySelectorAll(
      ".p-navigation__dropdown-content--sliding .js-back-button"
    )
    .forEach((btn) => {
      addMobileListener(btn, "click", () => trackMobileBackClick(btn));
    });

  // Mobile: top-level section toggles (Products, Solutions, etc.)
  root
    .querySelectorAll(".js-dropdown-button[data-level='0']")
    .forEach((a) => {
      addMobileListener(a, "click", () => trackMobileLevel1ToggleClick(a));
    });

  // Mobile: nav_section toggles inside a top-level section
  root
    .querySelectorAll(
      ".p-navigation__dropdown-content--sliding .p-navigation__item--dropdown-toggle > a.js-dropdown-button[data-level='1']"
    )
    .forEach((a) => {
      addMobileListener(a, "click", () => trackMobileNavSectionToggleClick(a));
    });

  // Mobile: external navigation clicks (links leading out of the menu)
  root
    .querySelectorAll(".p-navigation__dropdown-content--sliding a")
    .forEach((a) => {
      // Ignore menu-internal controls
      if (
        a.classList.contains("js-back-button") ||
        a.classList.contains("js-dropdown-button") ||
        (a.getAttribute("href") || "").startsWith("#")
      ) {
        return;
      }
      addMobileListener(a, "click", () => trackMobileExternalLinkClick(a));
    });
}
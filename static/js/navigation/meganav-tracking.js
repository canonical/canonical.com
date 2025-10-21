import { navigation, topLevelNavigationItems } from "./elements";

// Performance caches and helpers for desktop tracking
let desktopTopbarButtons = [];
const desktopTopbarByControls = new Map(); // controls/id -> { index, el }

function buildDesktopTopbarCache() {
  const list = topLevelNavigationItems;
  if (!list || desktopTopbarButtons.length) return;
  desktopTopbarButtons = Array.from(
    list.querySelectorAll(
      ".p-navigation__item--dropdown-toggle > .js-dropdown-button"
    )
  );
  desktopTopbarButtons.forEach((el, i) => {
    const controls = el.getAttribute("aria-controls") || "";
    if (controls) {
      desktopTopbarByControls.set(controls, { index: i + 1, el });
      // Also map the id without "-content" to match dropdown window ids
      if (controls.endsWith("-content")) {
        desktopTopbarByControls.set(
          controls.slice(0, -"-content".length),
          { index: i + 1, el }
        );
      }
    }
  });
}

function indexBySelector(el, selector) {
  let idx = 0;
  let node = el;
  while (node) {
    if (node.matches && node.matches(selector)) idx += 1;
    node = node.previousElementSibling;
  }
  return idx;
}

function ensureDataLayer() {
  if (!window.dataLayer) {
    window.dataLayer = [];
  }
}

function textify(el) {
  if (!el) return "";
  return (el.textContent || "").trim();
}

function getLinkTitle(a) {
  if (!a) return "";
  const span = a.querySelector("span");
  if (span) return textify(span);
  const directText = Array.from(a.childNodes)
    .filter((n) => n.nodeType === Node.TEXT_NODE)
    .map((n) => (n.textContent || "").trim())
    .join(" ")
    .trim();
  if (directText) return directText;
  const clone = a.cloneNode(true);
  clone.querySelectorAll("small, br").forEach((el) => el.remove());
  return (clone.textContent || "").trim();
}

function segmentString(index, label) {
  const safeLabel = (label || "").toLowerCase();
  return `${index}. ${safeLabel}`;
}

function getTopbarInfo(contextEl) {
  buildDesktopTopbarCache();
  const list = topLevelNavigationItems;
  if (!list) return null;

  // If context is within a dropdown window, map its id back to the button
  const dropdownWindow = contextEl?.closest?.(".js-dropdown-window");
  if (dropdownWindow && dropdownWindow.id) {
    const cached = desktopTopbarByControls.get(dropdownWindow.id);
    if (cached) {
      return { index: cached.index, label: textify(cached.el) };
    }
  }

  // Otherwise, use the active topbar item if available
  const active = list.querySelector(".is-active > .js-dropdown-button") || null;
  if (active) {
    const idx = desktopTopbarButtons.indexOf(active) + 1;
    return { index: idx, label: textify(active) };
  }
  return null;
}

function getSidebarInfo(contextEl) {
  const dropdownWindow = contextEl?.closest?.(".js-dropdown-window");
  if (!dropdownWindow) return null;
  const tabsList = dropdownWindow.querySelector(
    ".p-side-navigation__list.js-tabs"
  );
  if (!tabsList) return null;
  const active = tabsList.querySelector(
    ".p-side-navigation__link.js-navigation-tab.is-active"
  );
  if (!active) return null;
  const idx = indexBySelector(active, ".p-side-navigation__link.js-navigation-tab");
  return { index: idx, label: textify(active) };
}

function getGroupInfo(contextEl) {
  const dropdownWindow = contextEl?.closest?.(".js-dropdown-window");
  if (!dropdownWindow) return null;
  const active = dropdownWindow.querySelector(
    ".p-side-navigation__link.js-navigation-tab.is-active"
  );
  if (!active) return null;
  const targetId = active.getAttribute("aria-controls");
  const windowForTab = dropdownWindow.querySelector(`#${targetId}`);
  const headings = windowForTab?.querySelectorAll?.(
    "li.p-navigation--list-heading"
  );
  if (!windowForTab || !headings?.length) return null;
  const listItem = contextEl.closest("li");
  if (!listItem) return null;
  let headingEl = null;
  let prev = listItem.previousElementSibling;
  while (prev) {
    if (prev.matches("li.p-navigation--list-heading")) {
      headingEl = prev;
      break;
    }
    prev = prev.previousElementSibling;
  }
  if (headingEl) {
    const idx = indexBySelector(headingEl, "li.p-navigation--list-heading");
    const labelEl =
      headingEl.querySelector(".p-navigation__dropdown-item") || headingEl;
    return { index: idx, label: textify(labelEl) };
  }
  return null;
}

function getItemInfo(target) {
  const listItem = target.closest("li");
  if (listItem && listItem.parentElement) {
    // Compute index without building arrays; ignore close items
    let idx = 0;
    let node = listItem.parentElement.firstElementChild;
    while (node) {
      if (!node.matches(".p-navigation__item--dropdown-close")) {
        idx += 1;
      }
      if (node === listItem) break;
      node = node.nextElementSibling;
    }
    return { index: idx, label: getLinkTitle(target) };
  }

  // Preview links grid
  const previewLink = target.closest(".p-navigation__preview-link");
  if (previewLink) {
    const container = previewLink.closest(
      ".p-navigation__preview-links, .p-navigation__preview-link--container"
    );
    if (container) {
      // Compute index by counting previous matching siblings
      let idx = 0;
      let node = container.firstElementChild;
      while (node) {
        if (node.matches && node.matches("a.p-navigation__preview-link")) {
          idx += 1;
        }
        if (node === previewLink) break;
        node = node.nextElementSibling;
      }
      return { index: idx, label: getLinkTitle(previewLink) };
    }
  }

  return { index: 0, label: getLinkTitle(target) };
}

function push(values) {
  ensureDataLayer();
  window.dataLayer.push(values);
}

function buildBaseValues() {
  return { event: "meganav click desktop" };
}

function handleTopbarClick(a) {
  const topbar = getTopbarInfo(a);
  if (!topbar) return;
  const values = buildBaseValues();
  values.mega_nav_area = "topbar";
  values.click_label = segmentString(topbar.index, topbar.label);
  values.mega_nav_path = values.click_label;
  push(values);
}

function handleSidebarClick(a) {
  const topbar = getTopbarInfo(a);
  const sidebar = getSidebarInfo(a);
  if (!topbar || !sidebar) return;
  const values = buildBaseValues();
  values.mega_nav_area = "sidebar";
  const sidebarSeg = segmentString(sidebar.index, sidebar.label);
  const topbarSeg = segmentString(topbar.index, topbar.label);
  values.click_label = sidebarSeg;
  values.mega_nav_path = `${topbarSeg} | ${sidebarSeg}`;
  push(values);
}

function handleDropdownLinkClick(a) {
  const topbar = getTopbarInfo(a);
  const group = getGroupInfo(a);
  const item = getItemInfo(a);
  if (!topbar || !item) return;
  const values = buildBaseValues();
  values.mega_nav_area = "dropdown";
  const itemSeg = segmentString(item.index, item.label);
  const topbarSeg = segmentString(topbar.index, topbar.label);
  const parts = [topbarSeg];
  if (group && group.label) parts.push(segmentString(group.index, group.label));
  parts.push(itemSeg);
  values.click_label = itemSeg;
  values.mega_nav_path = parts.join(" | ");
  push(values);
}

export default function initMeganavTracking() {
  const root = navigation;
  if (!root) return;

  const init = () => {
    buildDesktopTopbarCache();

    root.addEventListener(
      "click",
      (e) => {
        const target = e.target.closest("a, button");
        if (!target) return;

        // Desktop topbar toggles (exclude mobile sliding context)
        if (
          target.matches(
            ".p-navigation__item--dropdown-toggle > .js-dropdown-button"
          ) && !target.closest(".p-navigation__dropdown-content--sliding")
        ) {
          handleTopbarClick(target);
          return;
        }

        // Sidebar tabs within dropdown window
        if (
          target.matches(".js-navigation-tab") &&
          target.closest(".js-dropdown-window")
        ) {
          handleSidebarClick(target);
          return;
        }

        // Links inside dropdowns: primary, secondary, and preview links
        if (
          target.closest(".js-dropdown-window") &&
          (target.matches("a.p-navigation__dropdown-item") ||
            target.matches(".p-navigation__link-list a") ||
            target.matches("a.p-navigation__preview-link"))
        ) {
          handleDropdownLinkClick(target);
          return;
        }
      },
      { capture: false }
    );
  };

  if ("requestIdleCallback" in window) {
    window.requestIdleCallback(init);
  } else {
    setTimeout(init, 0);
  }
}

export { push, segmentString, textify, getLinkTitle };
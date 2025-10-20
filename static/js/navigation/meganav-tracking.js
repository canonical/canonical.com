import { navigation, topLevelNavigationItems } from "./elements";

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
  // Prefer direct text nodes to avoid nested <small> descriptions
  const directText = Array.from(a.childNodes)
    .filter((n) => n.nodeType === Node.TEXT_NODE)
    .map((n) => (n.textContent || "").trim())
    .join(" ")
    .trim();
  if (directText) return directText;
  // As a fallback, remove known non-title elements and read remaining text
  const clone = a.cloneNode(true);
  clone.querySelectorAll("small, br").forEach((el) => el.remove());
  return (clone.textContent || "").trim();
}

function segmentString(index, label) {
  const safeLabel = (label || "").toLowerCase();
  return `${index}. ${safeLabel}`;
}

function getTopbarInfo(contextEl) {
  const list = topLevelNavigationItems;
  if (!list) return null;
  const items = Array.from(
    list.querySelectorAll(
      ".p-navigation__item--dropdown-toggle > .js-dropdown-button"
    )
  );

  // If context is within a dropdown window, map its id back to the control button
  const dropdownWindow = contextEl?.closest?.(".js-dropdown-window");
  if (dropdownWindow && dropdownWindow.id) {
    const control = list.querySelector(
      `.js-dropdown-button[aria-controls="${dropdownWindow.id}-content"]`
    );
    if (control) {
      const idx = items.indexOf(control) + 1;
      return { index: idx, label: textify(control) };
    }
  }

  // Otherwise, use the active topbar item if available
  const active = list.querySelector(".is-active > .js-dropdown-button") || null;
  const target = active || null;
  if (target) {
    const idx = items.indexOf(target) + 1;
    return { index: idx, label: textify(target) };
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
  const tabs = Array.from(
    tabsList.querySelectorAll(".p-side-navigation__link.js-navigation-tab")
  );
  const active = tabsList.querySelector(
    ".p-side-navigation__link.js-navigation-tab.is-active"
  );
  if (!active) return null;
  const idx = tabs.indexOf(active) + 1;
  return { index: idx, label: textify(active) };
}

function getGroupInfo(contextEl) {
  const dropdownWindow = contextEl?.closest?.(".js-dropdown-window");
  if (!dropdownWindow) return null;
  const container = contextEl.closest(
    ".p-navigation__main-links, .p-navigation__link-list, .p-navigation__preview-links"
  );
  if (!container) return null;
  const allGroups = Array.from(
    dropdownWindow.querySelectorAll(
      ".p-navigation__main-links, .p-navigation__link-list, .p-navigation__preview-links"
    )
  );
  const idx = allGroups.indexOf(container) + 1;
  // Prefer a heading if available
  const heading = container.querySelector(
    ".p-navigation--list-heading, .p-navigation--list-heading a"
  );
  let label = heading ? textify(heading) : "";
  return { index: idx, label };
}

function getItemInfo(target) {
  // Primary/secondary list items
  const listItem = target.closest("li");
  if (listItem && listItem.parentElement) {
    const siblings = Array.from(listItem.parentElement.children);
    const idx = siblings.indexOf(listItem) + 1;
    return { index: idx, label: getLinkTitle(target) };
  }

  // Preview links grid
  const previewLink = target.closest(".p-navigation__preview-link");
  if (previewLink) {
    const container = previewLink.closest(
      ".p-navigation__preview-links, .p-navigation__preview-link--container"
    );
    if (container) {
      const anchors = Array.from(
        container.querySelectorAll("a.p-navigation__preview-link")
      );
      const idx = anchors.indexOf(previewLink) + 1;
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
  if (!topbar) return;
  const values = buildBaseValues();
  // Links live in the dropdown content area; classify under topbar
  values.mega_nav_area = "topbar";

  const item = getItemInfo(a);
  const itemSeg = segmentString(item.index, item.label);
  values.click_label = itemSeg;

  const topbarSeg = segmentString(topbar.index, topbar.label);
  const sidebar = getSidebarInfo(a);
  const group = getGroupInfo(a);
  const parts = [topbarSeg];
  if (sidebar) parts.push(segmentString(sidebar.index, sidebar.label));
  if (group && group.label) parts.push(segmentString(group.index, group.label));
  parts.push(itemSeg);
  values.mega_nav_path = parts.join(" | ");

  if (a.href) {
    values.click_from = window.location.origin;
    values.click_to = a.href;
  }

  push(values);
}

export default function initMeganavTracking() {
  const root = navigation;
  if (!root) return;

  // Topbar toggle buttons
  root
    .querySelectorAll(
      ".js-show-nav > .js-dropdown-list > .p-navigation__item--dropdown-toggle > a.js-dropdown-button"
    )
    .forEach((a) => {
      a.addEventListener("click", () => handleTopbarClick(a));
    });

  // Sidebar tabs within any dropdown window
  root.querySelectorAll(".js-dropdown-window .js-navigation-tab").forEach((a) => {
    a.addEventListener("click", () => handleSidebarClick(a));
  });

  // Links inside dropdowns: primary, secondary, and preview links
  root
    .querySelectorAll(
      ".js-dropdown-window a.p-navigation__dropdown-item, .js-dropdown-window .p-navigation__link-list a, .js-dropdown-window a.p-navigation__preview-link"
    )
    .forEach((a) => {
      a.addEventListener("click", () => handleDropdownLinkClick(a));
    });
}
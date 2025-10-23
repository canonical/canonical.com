import { navigation, topLevelNavigationItems } from "./elements";
import {
  ensureDataLayerInitialized,
  getText,
  getElementTitle,
  formatSegment,
  joinSegments,
  pushToDataLayer
} from "./utils";

function findDropdownWindow(contextEl) {
  return contextEl?.closest?.(".js-dropdown-window") || null;
}

function getTopbarSegment(contextEl) {
  const listEl = topLevelNavigationItems;
 if (!listEl) return null;

  const topbarButtons = Array.from(
    listEl.querySelectorAll(
      "[role='menuitem'].p-navigation__item--dropdown-toggle > .js-dropdown-button"
    )
  );

  // If the clicked element itself is a topbar button, use it directly
  if (contextEl?.matches?.(".js-dropdown-button")) {
    const index = topbarButtons.indexOf(contextEl) + 1;
    if (index > 0) {
      return { index, label: getText(contextEl) };
    }
  }

  // If context is within a dropdown window, map its id back to the topbar control button
  const dropdownWindow = findDropdownWindow(contextEl);
  if (dropdownWindow && dropdownWindow.id) {
    const controlButton = listEl.querySelector(
      `.js-dropdown-button[aria-controls="${dropdownWindow.id}-content"]`
    );
    if (controlButton) {
      const index = topbarButtons.indexOf(controlButton) + 1;
      return { index, label: getText(controlButton) };
    }
  }

  // Otherwise, use the active topbar item if available
  const activeButton = listEl.querySelector(".is-active > .js-dropdown-button");
  if (activeButton) {
    const index = topbarButtons.indexOf(activeButton) + 1;
    return { index, label: getText(activeButton) };
  }

  return null;
}

function getSidebarSegment(contextEl) {
  const dropdownWindow = findDropdownWindow(contextEl);
  if (!dropdownWindow) return null;

  const tabsList = dropdownWindow.querySelector(
    ".p-side-navigation__list.js-tabs"
  );
  if (!tabsList) return null;

  const tabs = Array.from(
    tabsList.querySelectorAll(".p-side-navigation__link.js-navigation-tab")
  );
  const activeTab = tabsList.querySelector(
    ".p-side-navigation__link.js-navigation-tab.is-active"
  );
  if (!activeTab) return null;

  const index = tabs.indexOf(activeTab) + 1;
  return { index, label: getText(activeTab) };
}

function getGroupSegment(contextEl) {
  const dropdownWindow = findDropdownWindow(contextEl);
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
  const index = allGroups.indexOf(container) + 1;
  const heading = container.querySelector(
    ".p-navigation--list-heading, .p-navigation--list-heading a"
  );
  const label = heading ? getText(heading) : "";

  return { index, label };
}

function getItemSegment(targetEl) {
  // Primary/secondary list items
  const listItem = targetEl.closest("li");
  if (listItem && listItem.parentElement) {
    const siblings = Array.from(listItem.parentElement.children);
    const index = siblings.indexOf(listItem) + 1;
    return { index, label: getElementTitle(targetEl) };
  }

  // Preview links grid
  const previewLink = targetEl.closest(".p-navigation__preview-link");
  if (previewLink) {
    const container = previewLink.closest(
      ".p-navigation__preview-links, .p-navigation__preview-link--container"
    );
    if (container) {
      const anchors = Array.from(
        container.querySelectorAll("a.p-navigation__preview-link")
      );
      const index = anchors.indexOf(previewLink) + 1;
      return { index, label: getElementTitle(previewLink) };
    }
  }

  return { index: -1, label: getElementTitle(targetEl) };
}

function buildBaseEvent() {
  return { event: "meganav click desktop" };
}

function buildClickEvent({ area, pathSegments, clickLabel, href }) {
  const values = buildBaseEvent();
  values.mega_nav_area = area;
  values.click_label = clickLabel;
  values.mega_nav_path = joinSegments(pathSegments);

  if (href) {
    values.click_from = window.location.origin;
    values.click_to = href;
  }
  return values;
}

function trackTopbarClick(linkEl) {
  const topbar = getTopbarSegment(linkEl);
  if (!topbar) return;

  const topbarSeg = formatSegment(topbar.index, topbar.label);
  const values = buildClickEvent({
    area: "topbar",
    pathSegments: [topbarSeg],
    clickLabel: topbarSeg,
    href: null,
  });

  pushToDataLayer(values);
}

function trackSidebarClick(linkEl) {
  const topbar = getTopbarSegment(linkEl);
  const sidebar = getSidebarSegment(linkEl);
  if (!topbar || !sidebar) return;

  const topbarSeg = formatSegment(topbar.index, topbar.label);
  const sidebarSeg = formatSegment(sidebar.index, sidebar.label);
  const values = buildClickEvent({
    area: "sidebar",
    pathSegments: [topbarSeg, sidebarSeg],
    clickLabel: sidebarSeg,
    href: null,
  });

  pushToDataLayer(values);
}

function trackDropdownLinkClick(linkEl) {
  const topbar = getTopbarSegment(linkEl);
  if (!topbar) return;

  const item = getItemSegment(linkEl);
  const itemSeg = formatSegment(item.index, item.label);
  const topbarSeg = formatSegment(topbar.index, topbar.label);
  const sidebar = getSidebarSegment(linkEl);
  const group = getGroupSegment(linkEl);

  const pathSegments = [topbarSeg];
  if (sidebar) pathSegments.push(formatSegment(sidebar.index, sidebar.label));
  if (group && group.label && group.index > 0) pathSegments.push(formatSegment(group.index, group.label));
  pathSegments.push(itemSeg);

  const values = buildClickEvent({
    area: "topbar",
    pathSegments,
    clickLabel: itemSeg,
    href: linkEl.href || null,
  });

  pushToDataLayer(values);
}

// ============================================================================
// Search Tracking Functions
// ============================================================================
function trackSearchClick(label) {
  const values = buildBaseEvent();
  values.mega_nav_area = "search";
  values.click_label = label;
  values.mega_nav_path = label;
  pushToDataLayer(values);
}

export default function initMeganavTracking() {
  const root = navigation;
  if (!root) return;

  // Topbar toggle buttons
  root
    .querySelectorAll(
      ".js-show-nav > .js-dropdown-list > .p-navigation__item--dropdown-toggle > a.js-dropdown-button"
    )
    .forEach((linkEl) => {
      linkEl.addEventListener("click", () => trackTopbarClick(linkEl));
    });

  // Sidebar tabs within any dropdown window
  root
    .querySelectorAll(".js-dropdown-window .js-navigation-tab")
    .forEach((linkEl) => {
      linkEl.addEventListener("click", () => trackSidebarClick(linkEl));
    });

  // Links inside dropdowns: primary, secondary, and preview links
  root
    .querySelectorAll(
      ".js-dropdown-window a.p-navigation__dropdown-item, .js-dropdown-window .p-navigation__link-list a, .js-dropdown-window a.p-navigation__preview-link"
    )
    .forEach((linkEl) => {
      linkEl.addEventListener("click", () => trackDropdownLinkClick(linkEl));
    });

  // ============================================================================
  // Search Event Listeners (click-only per requirements)
  // ============================================================================

  // Search toggle button clicks
  root
    .querySelectorAll(".js-search-button.p-navigation__link--search-toggle")
    .forEach((buttonEl) => {
      buttonEl.addEventListener("click", () => trackSearchClick("search toggle"));
    });

  // Track when the search input is clicked/focused to type
  root
    .querySelectorAll(".p-search-box__input")
    .forEach((inputEl) => {
      inputEl.addEventListener("focus", () => trackSearchClick("search input focused"));
    });

  // Track clicks on the close/reset icon button
  root
    .querySelectorAll(".p-search-box__reset")
    .forEach((resetEl) => {
      resetEl.addEventListener("click", () => trackSearchClick("search reset"));
    });
}
// File containing the elements that are used in a lot of place
// Keeps a single source of truth

export const navigation = document.querySelector(
  ".p-navigation--sliding, .p-navigation--reduced"
);

export const secondaryNavigation = document.querySelector(
  ".p-navigation.is-secondary"
);

export const topLevelNavigationItems =
  document.querySelector(".js-show-nav > ul");

export const toggles = document.querySelectorAll(".js-dropdown-button");

export const lists = navigation.querySelectorAll(".js-dropdown-list");

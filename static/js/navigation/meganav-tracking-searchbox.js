import { navigation } from "./elements";
import { pushToDataLayer } from "./utils";

function trackSearchClick(label) {
  const values = { event: "meganav click" };
  values.mega_nav_area = "search";
  values.click_label = label;
  values.mega_nav_path = label;
  pushToDataLayer(values);
}

export default function initMeganavSearchTracking() {
  const root = navigation;
  if (!root) return;

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
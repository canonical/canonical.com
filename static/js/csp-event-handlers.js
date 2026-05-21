(function () {
  "use strict";

  function ready(fn) {
    if (document.readyState !== "loading") {
      fn();
    } else {
      document.addEventListener("DOMContentLoaded", fn);
    }
  }

  function pushDataLayer(el) {
    if (typeof window.dataLayer === "undefined") {
      window.dataLayer = [];
    }
    var category = el.getAttribute("data-ga-category");
    var action = el.getAttribute("data-ga-action");
    var label = el.getAttribute("data-ga-label");
    var extra = el.getAttribute("data-ga-extra-category");
    var extraAction = el.getAttribute("data-ga-extra-action");
    var extraLabel = el.getAttribute("data-ga-extra-label");
    if (category && action) {
      window.dataLayer.push({
        event: "GAEvent",
        eventCategory: category,
        eventAction: action,
        eventLabel: label || undefined,
        eventValue: undefined,
      });
    }
    if (extra && extraAction) {
      window.dataLayer.push({
        event: "GAEvent",
        eventCategory: extra,
        eventAction: extraAction,
        eventLabel: extraLabel || undefined,
        eventValue: undefined,
      });
    }
  }

  ready(function () {
    document.querySelectorAll("[data-ga-category]").forEach(function (el) {
      el.addEventListener("click", function () {
        pushDataLayer(el);
      });
    });

    document
      .querySelectorAll("[data-ga-submit-category]")
      .forEach(function (form) {
        form.addEventListener("submit", function () {
          if (typeof window.dataLayer === "undefined") {
            window.dataLayer = [];
          }
          window.dataLayer.push({
            event: "GAEvent",
            eventCategory: form.getAttribute("data-ga-submit-category"),
            eventAction: form.getAttribute("data-ga-submit-action"),
            eventLabel:
              form.getAttribute("data-ga-submit-label") || undefined,
            eventValue: undefined,
          });
        });
      });
  });
})();

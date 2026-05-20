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

    document.querySelectorAll("[data-js-hide-target]").forEach(function (el) {
      el.addEventListener("click", function (event) {
        event.preventDefault();
        var target = document.querySelector(
          el.getAttribute("data-js-hide-target")
        );
        if (target) {
          target.classList.add("u-hide");
        }
      });
    });

    function toggleProgressDetail(stage, show) {
      var showMoreBtn = document.querySelector(".show-more-" + stage);
      var showLessBtn = document.querySelector(".show-less-" + stage);
      var details = document.querySelectorAll(".progress-detail-" + stage);
      details.forEach(function (detail) {
        if (show && detail.classList.contains("u-hide")) {
          detail.classList.remove("u-hide");
          if (showMoreBtn) showMoreBtn.classList.add("u-hide");
          if (showLessBtn) showLessBtn.classList.remove("u-hide");
        } else if (!show && !detail.classList.contains("u-hide")) {
          detail.classList.add("u-hide");
          if (showMoreBtn) showMoreBtn.classList.remove("u-hide");
          if (showLessBtn) showLessBtn.classList.add("u-hide");
        }
      });
    }

    document
      .querySelectorAll("[data-js-progress-show]")
      .forEach(function (el) {
        el.addEventListener("click", function (event) {
          event.preventDefault();
          toggleProgressDetail(el.getAttribute("data-js-progress-show"), true);
        });
      });

    document
      .querySelectorAll("[data-js-progress-hide]")
      .forEach(function (el) {
        el.addEventListener("click", function (event) {
          event.preventDefault();
          toggleProgressDetail(
            el.getAttribute("data-js-progress-hide"),
            false
          );
        });
      });

    document
      .querySelectorAll("[data-js-clear-prev-input]")
      .forEach(function (el) {
        el.addEventListener("click", function () {
          var prev = el.previousElementSibling;
          if (prev) {
            prev.value = "";
            prev.focus();
          }
        });
      });

    document
      .querySelectorAll("[data-js-navigate-on-change]")
      .forEach(function (el) {
        el.addEventListener("change", function () {
          if (el.value) {
            window.location.href = el.value;
          }
        });
      });
  });
})();

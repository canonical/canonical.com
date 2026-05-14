/**
 * Delegated event handlers that replace inline on*= attributes across
 * the site. Loading this once lets us drop 'unsafe-inline' from
 * script-src (it stops being needed for inline event-handler execution).
 *
 * All handlers are attached to `document` and use ancestor matching, so
 * elements rendered later (e.g. by HTMX-ish replacements or by the
 * watch-consent-changes module) are covered automatically.
 *
 * Conventions:
 *   - Analytics:   data-ga-event / data-ga-category / data-ga-action /
 *                  data-ga-label  (+ optional data-ga-extra-* for a
 *                  stacked second push, used on /maas/features).
 *   - Dismissal:   data-dismiss="#some-selector"   (click hides target)
 *   - Progress UI: data-progress-action="show|hide"
 *                  data-progress-target="<group-name>"
 *   - Clear input: data-action="clear-prev-input"  (clears prev sibling)
 *   - Submit GA:   data-ga-submit-category / data-ga-submit-action /
 *                  data-ga-submit-label  on the <form>.
 */
(function () {
  "use strict";

  function ancestorWith(el, attr) {
    while (el && el.nodeType === 1) {
      if (el.hasAttribute && el.hasAttribute(attr)) return el;
      el = el.parentElement;
    }
    return null;
  }

  function pushGAEvent(el, prefix) {
    if (!window.dataLayer) return;
    var get = function (suffix) {
      return el.getAttribute("data-ga-" + prefix + suffix);
    };
    var name = get("event");
    if (!name) return;
    window.dataLayer.push({
      event: name,
      eventCategory: get("category"),
      eventAction: get("action"),
      eventLabel: get("label"),
    });
  }

  document.addEventListener("click", function (event) {
    // --- GA dataLayer push on click ---
    var gaEl = ancestorWith(event.target, "data-ga-event");
    if (gaEl) {
      pushGAEvent(gaEl, "");
      // Some elements stack a second event (the "Interested in feature"
      // pattern on /maas/features). Encoded via data-ga-extra-*.
      if (gaEl.hasAttribute("data-ga-extra-event")) {
        pushGAEvent(gaEl, "extra-");
      }
    }

    // --- Dismissal: hide the targeted element ---
    var dismissEl = ancestorWith(event.target, "data-dismiss");
    if (dismissEl) {
      var dismissTarget = document.querySelector(
        dismissEl.getAttribute("data-dismiss")
      );
      if (dismissTarget) dismissTarget.classList.add("u-hide");
    }

    // --- Career application progress toggles ---
    var progEl = ancestorWith(event.target, "data-progress-action");
    if (progEl) {
      var action = progEl.getAttribute("data-progress-action");
      var target = progEl.getAttribute("data-progress-target");
      if (
        action === "show" &&
        typeof window.showProgressDetail === "function"
      ) {
        window.showProgressDetail(target);
        event.preventDefault();
      } else if (
        action === "hide" &&
        typeof window.hideProgressDetail === "function"
      ) {
        window.hideProgressDetail(target);
        event.preventDefault();
      }
    }

    // --- Clear-previous-sibling-input (search input clear button) ---
    var actionEl = ancestorWith(event.target, "data-action");
    if (
      actionEl &&
      actionEl.getAttribute("data-action") === "clear-prev-input"
    ) {
      var input = actionEl.previousElementSibling;
      if (input) {
        input.value = "";
        input.focus();
      }
    }

    // --- Load-more buttons (juju search) ---
    var loadMoreEl = ancestorWith(event.target, "data-action");
    if (
      loadMoreEl &&
      loadMoreEl.getAttribute("data-action") === "load-more-results" &&
      typeof window.loadMoreResults === "function"
    ) {
      window.loadMoreResults();
    }
  });

  // --- Form submit: GA send (legacy ga() and dataLayer push) ---
  document.addEventListener(
    "submit",
    function (event) {
      var form = event.target;
      if (!form || !form.hasAttribute) return;

      // Forms that previously dispatched dataLayer.push() inline carry
      // data-ga-submit-event="GAEvent" (the explicit event name).
      if (form.hasAttribute("data-ga-submit-event") && window.dataLayer) {
        window.dataLayer.push({
          event: form.getAttribute("data-ga-submit-event"),
          eventCategory: form.getAttribute("data-ga-submit-category"),
          eventAction: form.getAttribute("data-ga-submit-action"),
          eventLabel: form.getAttribute("data-ga-submit-label"),
        });
      } else if (form.hasAttribute("data-ga-submit-category")) {
        // Legacy ga('send', category, action, label) — no explicit event
        // name, so call ga() if available and also push to dataLayer.
        if (typeof window.ga === "function") {
          window.ga(
            "send",
            form.getAttribute("data-ga-submit-category"),
            form.getAttribute("data-ga-submit-action"),
            form.getAttribute("data-ga-submit-label")
          );
        }
        if (window.dataLayer) {
          window.dataLayer.push({
            event: "form-submit",
            eventCategory: form.getAttribute("data-ga-submit-category"),
            eventAction: form.getAttribute("data-ga-submit-action"),
            eventLabel: form.getAttribute("data-ga-submit-label"),
          });
        }
      }

      // Custom hook: data-on-submit="getCustomFields"
      var hook = form.getAttribute("data-on-submit");
      if (hook && typeof window[hook] === "function") {
        window[hook](event);
      }
    },
    true
  );

  // --- onchange="showInput()" replacement (forms/form-fields.html) ---
  document.addEventListener("change", function (event) {
    var el = event.target;
    if (!el || !el.getAttribute) return;
    var hook = el.getAttribute("data-on-change");
    if (hook && typeof window[hook] === "function") {
      window[hook](event);
    }
  });
})();

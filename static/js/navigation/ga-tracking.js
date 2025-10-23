import initMeganavTracking, { destroyMeganavTracking } from "./meganav-tracking";
import initMeganavTrackingMobile, { destroyMeganavTrackingMobile } from "./meganav-tracking-mobile";
import { isDesktop } from "./utils";

// Track current mode and ensure we only attach one resize listener
let isCurrentlyDesktop = null;
let resizeListenerRegistered = false;

export default function initGATracking() {
  // Initialize tracking based on the current breakpoint.
  if (isDesktop()) {
    initMeganavTracking();
    isCurrentlyDesktop = true;
  } else {
    initMeganavTrackingMobile();
    isCurrentlyDesktop = false;
  }

  // Listen for resize events to reinitialize tracking if the breakpoint changes.
  if (!resizeListenerRegistered) {
    window.addEventListener("resize", () => {
      const isNowDesktop = isDesktop();

      // Do nothing if the breakpoint hasn't changed
      if (isNowDesktop === isCurrentlyDesktop) {
        return;
      }

      // Destroy the old tracker and initialize the new one.
      if (isNowDesktop) {
        destroyMeganavTrackingMobile();
        initMeganavTracking();
      } else {
        destroyMeganavTracking();
        initMeganavTrackingMobile();
      }

      // Update the current breakpoint.
      isCurrentlyDesktop = isNowDesktop;
    });
    resizeListenerRegistered = true;
  }

  addGAContentEvents("#main-content");

  function addGAContentEvents(target) {
    var t = document.querySelector(target);
    if (t) {
      t.querySelectorAll("a").forEach(function (a) {
        if (!a.href.startsWith("#")) {
          a.addEventListener("click", function () {
            const pushEvent = () => {
              // for buttons we get the origin from the current page
              var path = window.location.href.split("#");
              var actionOrigin = path[0];
              var actionTarget = window.location.href;
              if (a.className.includes("p-button--positive")) {
                var category = "canonical.com-content-cta-0";
              } else if (a.className.includes("p-button")) {
                var category = "canonical.com-content-cta-1";
              } else {
                var category = "canonical.com-content-link";
                actionOrigin = origin;
                actionTarget = a.href;
              }
              dataLayer.push({
                event: "GAEvent",
                eventCategory: category,
                eventAction: `from:${actionOrigin} to:${actionTarget}`,
                eventLabel: a.text,
                eventValue: undefined,
              });
            };
            // Wait briefly for form to open and location to change
            setTimeout(pushEvent, 500);
          });
        }
      });
    }
  }
}

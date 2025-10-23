import initMeganavTracking, { destroyMeganavTracking } from "./meganav-tracking";
import initMeganavTrackingMobile, { destroyMeganavTrackingMobile } from "./meganav-tracking-mobile";
import initMeganavSearchTracking from "./meganav-tracking-searchbox";

const mql = window.matchMedia("(min-width: 1035px)");
let isDesktopMode = mql.matches;

export default function initGATracking() {
  // Gate initialization by breakpoint at startup
  if (isDesktopMode) {
    initMeganavTracking();
  } else {
    initMeganavTrackingMobile();
  }
  initMeganavSearchTracking();

  mql.addEventListener("change", (e) => {
    const nextIsDesktop = e.matches;
    if (nextIsDesktop === isDesktopMode) return;

    if (nextIsDesktop) {
      destroyMeganavTrackingMobile();
      initMeganavTracking();
    } else {
      destroyMeganavTracking();
      initMeganavTrackingMobile();
    }
    isDesktopMode = nextIsDesktop;
  });

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

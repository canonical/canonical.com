export default function initGATracking() {
  addGANavEvents("#products-nav", "canonical.com-nav-products");
  addGANavEvents("#solutions-nav", "canonical.com-nav-solutions");
  addGANavEvents("#partners-nav", "canonical.com-nav-partners");
  addGANavEvents("#careers-nav", "canonical.com-nav-careers");
  addGANavEvents("#company-nav", "canonical.com-nav-careers");

  function addGANavEvents(target, category) {
    var t = document.querySelector(target);
    if (t) {
      t.querySelectorAll("a").forEach(function (a) {
        a.addEventListener("click", function () {
          dataLayer.push({
            event: "GAEvent",
            eventCategory: category,
            eventAction: `from:${origin} to:${a.href}`,
            eventLabel: a.text,
            eventValue: undefined,
          });
        });
      });
    }
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

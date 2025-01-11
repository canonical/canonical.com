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
        if (a.className.includes("p-button--positive")) {
          var category = "canonical.com-content-cta-0";
        } else if (a.className.includes("p-button")) {
          var category = "canonical.com-content-cta-1";
        } else {
          var category = "canonical.com-content-link";
        }
        if (!a.href.startsWith("#")) {
          a.addEventListener("click", function () {
            dataLayer.push({
              event: "GAEvent",
              eventCategory: category,
              eventAction: `from:${origin} to:${a.href}`,
              eventLabel: a.text,
              eventValue: undefined,
            });
          });
        }
      });
    }
  }
}

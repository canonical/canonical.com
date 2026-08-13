/** @jest-environment jsdom */
import { setUpDynamicSideNav } from "../../static/js/active-nav-scroll.js";

/**
 * Lays out a fake page so scroll position can be simulated in jsdom, which has
 * no layout engine. Each heading is given a fixed position in the document and
 * getBoundingClientRect() is derived from the current scroll offset.
 */
function buildPage({ viewportHeight, scrollHeight, headings, links }) {
  document.body.innerHTML = `
    <div class="p-side-navigation">
      ${links
        .map(
          (href) =>
            `<a class="p-side-navigation__link" href="${href}">${href}</a>`
        )
        .join("")}
    </div>
  `;

  headings.forEach(function (heading) {
    const element = document.createElement("h2");
    element.className = "section-heading";
    if (heading.id) {
      element.id = heading.id;
    }
    element.getBoundingClientRect = function () {
      const top = heading.docTop - window.scrollY;
      return { top: top, bottom: top + heading.height, height: heading.height };
    };
    document.body.appendChild(element);
  });

  Object.defineProperty(window, "innerHeight", {
    value: viewportHeight,
    configurable: true,
  });
  Object.defineProperty(document.documentElement, "scrollHeight", {
    value: scrollHeight,
    configurable: true,
  });
  setScroll(0);
}

function setScroll(y) {
  Object.defineProperty(window, "scrollY", { value: y, configurable: true });
}

function scrollTo(y) {
  setScroll(y);
  window.dispatchEvent(new Event("scroll"));
}

function activeLinks() {
  return Array.prototype.slice
    .call(document.querySelectorAll(".p-side-navigation__link"))
    .filter((link) => link.classList.contains("is-active"))
    .map((link) => link.getAttribute("href"));
}

describe("active-nav-scroll", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
    // Run animation frame callbacks synchronously so assertions can follow a
    // dispatched scroll event immediately.
    jest
      .spyOn(window, "requestAnimationFrame")
      .mockImplementation((callback) => {
        callback(0);
        return 0;
      });
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe("setUpDynamicSideNav function", () => {
    it("activates the section whose heading has passed the activation line", () => {
      buildPage({
        viewportHeight: 1000,
        scrollHeight: 5000,
        headings: [
          { id: "intro", docTop: 500, height: 100 },
          { id: "features", docTop: 1500, height: 100 },
          { id: "pricing", docTop: 2500, height: 100 },
        ],
        links: ["#intro", "#features", "#pricing"],
      });

      setUpDynamicSideNav();

      // "features" sits at docTop 1500, so it crosses the activation line
      // (13% of a 1000px viewport = 130px) once scrolled past 1370px.
      scrollTo(1400);
      expect(activeLinks()).toEqual(["#features"]);

      scrollTo(2400);
      expect(activeLinks()).toEqual(["#pricing"]);
    });

    it("activates the last link at the bottom of the page even when its heading never reaches the activation line", () => {
      // Regression test: the final section sits less than a viewport height
      // above the end of the document, so its heading can never be scrolled up
      // to the activation line. It must still become active.
      buildPage({
        viewportHeight: 1200,
        scrollHeight: 3000,
        headings: [
          { id: "intro", docTop: 600, height: 100 },
          { id: "middle", docTop: 1400, height: 100 },
          { id: "last", docTop: 2200, height: 100 },
        ],
        links: ["#intro", "#middle", "#last"],
      });

      setUpDynamicSideNav();

      // Maximum scroll is 3000 - 1200 = 1800, leaving "last" at 400px from the
      // top of the viewport, far below the 156px activation line.
      scrollTo(1800);
      expect(activeLinks()).toEqual(["#last"]);
    });

    it("ignores section headings that have no id so the nav is never blanked", () => {
      buildPage({
        viewportHeight: 1000,
        scrollHeight: 4000,
        headings: [
          { id: "intro", docTop: 500, height: 100 },
          { id: null, docTop: 2000, height: 100 },
        ],
        links: ["#intro"],
      });

      setUpDynamicSideNav();

      scrollTo(600);
      expect(activeLinks()).toEqual(["#intro"]);

      // Scrolling past the id-less heading must not clear the active link.
      scrollTo(2500);
      expect(activeLinks()).toEqual(["#intro"]);

      scrollTo(3000);
      expect(activeLinks()).toEqual(["#intro"]);
    });

    it("leaves the active state untouched above the first heading", () => {
      buildPage({
        viewportHeight: 1000,
        scrollHeight: 5000,
        headings: [{ id: "intro", docTop: 900, height: 100 }],
        links: ["#intro"],
      });

      setUpDynamicSideNav();

      scrollTo(100);
      expect(activeLinks()).toEqual([]);
    });

    it("recalculates when the viewport is resized", () => {
      buildPage({
        viewportHeight: 1000,
        scrollHeight: 5000,
        headings: [
          { id: "intro", docTop: 500, height: 100 },
          { id: "features", docTop: 1500, height: 100 },
        ],
        links: ["#intro", "#features"],
      });

      setUpDynamicSideNav();

      scrollTo(1300);
      expect(activeLinks()).toEqual(["#intro"]);

      // A taller viewport pushes the activation line down to 260px, which
      // "features" (at 200px) has now crossed.
      Object.defineProperty(window, "innerHeight", {
        value: 2000,
        configurable: true,
      });
      window.dispatchEvent(new Event("resize"));
      expect(activeLinks()).toEqual(["#features"]);
    });

    it("does not throw when there are no section headings or links", () => {
      document.body.innerHTML = "";
      expect(() => setUpDynamicSideNav()).not.toThrow();
    });

    it("handles sections with no corresponding navigation link", () => {
      buildPage({
        viewportHeight: 1000,
        scrollHeight: 5000,
        headings: [
          { id: "intro", docTop: 500, height: 100 },
          { id: "orphan", docTop: 1500, height: 100 },
        ],
        links: ["#intro"],
      });

      expect(() => setUpDynamicSideNav()).not.toThrow();

      scrollTo(600);
      expect(activeLinks()).toEqual(["#intro"]);

      // The orphan section has no link, so nothing should be highlighted.
      scrollTo(1400);
      expect(activeLinks()).toEqual([]);
    });
  });
});

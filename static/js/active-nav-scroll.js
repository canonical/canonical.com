/**
 * Marks the side navigation link of the section currently being read with
 * "is-active", derived from scroll position: the last "section-heading" to
 * have passed an activation line near the top of the viewport.
 *
 * Not an IntersectionObserver: a heading less than one viewport height from
 * the end of the document can never be scrolled up to that line, which left
 * the final links permanently unhighlighted.
 *
 * Links are matched to headings by href, e.g. href="#section-id".
 */

// Fraction of the viewport height a heading must pass to become current.
const ACTIVATION_LINE_RATIO = 0.13;

// Fractional layout heights mean the scroll offset rarely hits its max exactly.
const BOTTOM_TOLERANCE = 2;

export function setUpDynamicSideNav() {
  const sections = Array.prototype.slice
    .call(document.querySelectorAll(".section-heading"))
    // An id-less heading matches no link, so it would blank the whole nav.
    .filter(function (section) {
      return Boolean(section.id);
    });
  const navigationLinks = Array.prototype.slice.call(
    document.querySelectorAll(".p-side-navigation__link")
  );

  if (sections.length === 0 || navigationLinks.length === 0) {
    return;
  }

  function setActiveLink(sectionId) {
    navigationLinks.forEach(function (link) {
      if (link.getAttribute("href") === `#${sectionId}`) {
        link.classList.add("is-active");
      } else {
        link.classList.remove("is-active");
      }
    });
  }

  // The current heading, or null while still above the first one.
  function getCurrentSection() {
    const maxScroll =
      document.documentElement.scrollHeight - window.innerHeight;

    // Trailing headings may never reach the activation line, so once the page
    // can scroll no further the last section is the one on screen.
    if (maxScroll > 0 && window.scrollY >= maxScroll - BOTTOM_TOLERANCE) {
      return sections[sections.length - 1];
    }

    const activationLine = window.innerHeight * ACTIVATION_LINE_RATIO;
    let current = null;
    sections.forEach(function (section) {
      if (section.getBoundingClientRect().top <= activationLine) {
        current = section;
      }
    });
    return current;
  }

  function update() {
    const current = getCurrentSection();
    if (current) {
      setActiveLink(current.id);
    }
  }

  let updateQueued = false;
  function requestUpdate() {
    if (updateQueued) {
      return;
    }
    updateQueued = true;
    window.requestAnimationFrame(function () {
      updateQueued = false;
      update();
    });
  }

  window.addEventListener("scroll", requestUpdate, { passive: true });
  window.addEventListener("resize", requestUpdate);
  update();
}

setUpDynamicSideNav();

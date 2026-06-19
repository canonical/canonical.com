/** @jest-environment jsdom */
import { setUpDynamicSideNav } from "../../static/js/active-nav-scroll.js";

describe("active-nav-scroll", () => {
  let mockIntersectionObserver;
  let observerCallbacks = {};

  beforeEach(() => {
    // Clear the document
    document.body.innerHTML = "";

    // Reset callbacks
    observerCallbacks = {};

    // Mock IntersectionObserver
    mockIntersectionObserver = jest.fn((callback, options) => {
      return {
        observe: jest.fn(),
        unobserve: jest.fn(),
        disconnect: jest.fn(),
      };
    });

    global.IntersectionObserver = mockIntersectionObserver;
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  describe("setUpDynamicSideNav function", () => {
    it("should create IntersectionObserver for each section heading", () => {
      // Setup DOM
      document.body.innerHTML = `
        <div class="section-heading" id="section-1">Section 1</div>
        <div class="section-heading" id="section-2">Section 2</div>
        <div class="p-side-navigation__link" href="#section-1">Link 1</div>
        <div class="p-side-navigation__link" href="#section-2">Link 2</div>
      `;

      setUpDynamicSideNav();

      // Should create 2 observers (one for each section)
      expect(mockIntersectionObserver).toHaveBeenCalledTimes(2);
    });

    it("should set correct IntersectionObserver options", () => {
      document.body.innerHTML = `
        <div class="section-heading" id="section-1">Section 1</div>
        <div class="p-side-navigation__link" href="#section-1">Link 1</div>
      `;

      setUpDynamicSideNav();

      // Check that observer was created with correct options
      expect(mockIntersectionObserver).toHaveBeenCalledWith(
        expect.any(Function),
        {
          rootMargin: "-5% 0px -87% 0px",
          threshold: 0,
        }
      );
    });

    it("should add is-active class to matching link when section intersects", () => {
      document.body.innerHTML = `
        <div class="section-heading" id="section-1">Section 1</div>
        <div class="p-side-navigation__link" href="#section-1">Link 1</div>
        <div class="p-side-navigation__link" href="#section-2">Link 2</div>
      `;

      setUpDynamicSideNav();

      // Get the first observer callback (should be for section-1)
      const firstCallback = mockIntersectionObserver.mock.calls[0][0];

      // Simulate intersection
      const mockSection = document.querySelector(".section-heading");
      firstCallback([{ isIntersecting: true, target: mockSection }]);

      // Check that the correct link has is-active class
      const link1 = document.querySelector('[href="#section-1"]');
      const link2 = document.querySelector('[href="#section-2"]');

      expect(link1.classList.contains("is-active")).toBe(true);
      expect(link2.classList.contains("is-active")).toBe(false);
    });

    it("should remove is-active class from other links when section intersects", () => {
      document.body.innerHTML = `
        <div class="section-heading" id="section-1">Section 1</div>
        <div class="section-heading" id="section-2">Section 2</div>
        <div class="p-side-navigation__link is-active" href="#section-1">Link 1</div>
        <div class="p-side-navigation__link" href="#section-2">Link 2</div>
      `;

      setUpDynamicSideNav();

      // Get the second observer callback (should be for section-2)
      const secondCallback = mockIntersectionObserver.mock.calls[1][0];

      // Simulate intersection for section-2
      const mockSection = document.querySelector(".section-heading#section-2");
      secondCallback([{ isIntersecting: true, target: mockSection }]);

      // Check that link2 is active and link1 is not
      const link1 = document.querySelector('[href="#section-1"]');
      const link2 = document.querySelector('[href="#section-2"]');

      expect(link1.classList.contains("is-active")).toBe(false);
      expect(link2.classList.contains("is-active")).toBe(true);
    });

    it("should handle multiple sections correctly", () => {
      document.body.innerHTML = `
        <div class="section-heading" id="intro">Introduction</div>
        <div class="section-heading" id="features">Features</div>
        <div class="section-heading" id="pricing">Pricing</div>
        <div class="p-side-navigation__link" href="#intro">Intro</div>
        <div class="p-side-navigation__link" href="#features">Features</div>
        <div class="p-side-navigation__link" href="#pricing">Pricing</div>
      `;

      setUpDynamicSideNav();

      // Should create 3 observers
      expect(mockIntersectionObserver).toHaveBeenCalledTimes(3);

      // Test the features section becomes active
      const featuresSection = document.querySelector(".section-heading#features");
      const featureCallback = mockIntersectionObserver.mock.calls[1][0];
      featureCallback([{ isIntersecting: true, target: featuresSection }]);

      const links = document.querySelectorAll(".p-side-navigation__link");
      expect(links[0].classList.contains("is-active")).toBe(false); // intro
      expect(links[1].classList.contains("is-active")).toBe(true); // features
      expect(links[2].classList.contains("is-active")).toBe(false); // pricing
    });

    it("should not add is-active class when section is not intersecting", () => {
      document.body.innerHTML = `
        <div class="section-heading" id="section-1">Section 1</div>
        <div class="p-side-navigation__link" href="#section-1">Link 1</div>
      `;

      setUpDynamicSideNav();

      const callback = mockIntersectionObserver.mock.calls[0][0];
      const mockSection = document.querySelector(".section-heading");

      // Simulate non-intersecting entry
      callback([{ isIntersecting: false, target: mockSection }]);

      const link = document.querySelector('[href="#section-1"]');
      expect(link.classList.contains("is-active")).toBe(false);
    });

    it("should handle sections with no corresponding navigation links", () => {
      document.body.innerHTML = `
        <div class="section-heading" id="section-1">Section 1</div>
        <div class="section-heading" id="section-2">Section 2</div>
        <div class="p-side-navigation__link" href="#section-1">Link 1</div>
      `;

      expect(() => setUpDynamicSideNav()).not.toThrow();

      // Verify the function still works with section-1
      const section1 = document.querySelector(".section-heading#section-1");
      const callback = mockIntersectionObserver.mock.calls[0][0];
      callback([{ isIntersecting: true, target: section1 }]);

      const link = document.querySelector('[href="#section-1"]');
      expect(link.classList.contains("is-active")).toBe(true);
    });
  });
});

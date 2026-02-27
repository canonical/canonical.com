/** @jest-environment jsdom */
import { idFromTitle, generateTableOfContents } from "../../static/js/table-of-contents.js";

describe("table-of-contents", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
    delete window.location;
    window.location = { hash: "" };
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe("idFromTitle function", () => {
    it("should convert heading text to lowercase", () => {
      const result = idFromTitle("Hello World");
      expect(result).toBe("hello-world");
    });

    it("should replace spaces with hyphens", () => {
      const result = idFromTitle("This Is A Long Title");
      expect(result).toBe("this-is-a-long-title");
    });

    it("should handle multiple consecutive spaces", () => {
      const result = idFromTitle("Multiple   Spaces   Here");
      expect(result).toBe("multiple-spaces-here");
    });

    it("should handle commas and periods together", () => {
      const result = idFromTitle("Title. Comma, Period.");
      expect(result).toBe("title-comma-period");
    });

    it("should handle numbers in heading", () => {
      const result = idFromTitle("Section 123 Overview");
      expect(result).toBe("section-123-overview");
    });

    it("should handle single word", () => {
      const result = idFromTitle("Introduction");
      expect(result).toBe("introduction");
    });

    it("should handle empty string", () => {
      const result = idFromTitle("");
      expect(result).toBe("");
    });
  });

  describe("generateTableOfContents function", () => {
    it("should return early if content is missing", () => {
      const container = document.createElement("div");
      container.id = "table-of-contents";
      document.body.appendChild(container);

      generateTableOfContents(null, container);

      const list = container.querySelector(".p-table-of-contents__list");
      expect(list).toBeNull();
    });

    it("should return early if container is missing", () => {
      const content = document.createElement("div");
      content.className = "page-content";
      document.body.appendChild(content);

      generateTableOfContents(content, null);

      expect(document.querySelector(".p-table-of-contents__list")).toBeNull();
    });

    it("should create table of contents list with correct class", () => {
      const content = document.createElement("div");
      content.className = "page-content";
      const h2 = document.createElement("h2");
      h2.innerText = "Heading 1";
      content.appendChild(h2);

      const container = document.createElement("div");
      container.id = "table-of-contents";

      document.body.appendChild(content);
      document.body.appendChild(container);

      generateTableOfContents(content, container);

      const list = container.querySelector(".p-table-of-contents__list");
      expect(list).not.toBeNull();
      expect(list.tagName).toBe("UL");
    });

    it("should select h2, h3, and h4 headings", () => {
      const content = document.createElement("div");
      content.className = "page-content";

      const h1 = document.createElement("h1");
      h1.innerText = "Should not be included";
      const h2 = document.createElement("h2");
      h2.innerText = "Heading 2";
      const h3 = document.createElement("h3");
      h3.innerText = "Heading 3";
      const h4 = document.createElement("h4");
      h4.innerText = "Heading 4";
      const h5 = document.createElement("h5");
      h5.innerText = "Should not be included";

      content.appendChild(h1);
      content.appendChild(h2);
      content.appendChild(h3);
      content.appendChild(h4);
      content.appendChild(h5);

      const container = document.createElement("div");
      container.id = "table-of-contents";

      document.body.appendChild(content);
      document.body.appendChild(container);

      generateTableOfContents(content, container);

      const listItems = container.querySelectorAll(".p-table-of-contents__item");
      expect(listItems.length).toBe(3);
    });

    it("should generate IDs for headings from their text", () => {
      const content = document.createElement("div");
      content.className = "page-content";

      const h2 = document.createElement("h2");
      h2.innerText = "Getting Started";
      content.appendChild(h2);

      const container = document.createElement("div");
      container.id = "table-of-contents";

      document.body.appendChild(content);
      document.body.appendChild(container);

      generateTableOfContents(content, container);

      expect(h2.id).toBe("getting-started");
    });

    it("should set heading IDs correctly with multiple headings", () => {
      const content = document.createElement("div");
      content.className = "page-content";

      const h2a = document.createElement("h2");
      h2a.innerText = "First Section";
      const h2b = document.createElement("h2");
      h2b.innerText = "Second Section";
      const h3 = document.createElement("h3");
      h3.innerText = "Subsection";

      content.appendChild(h2a);
      content.appendChild(h2b);
      content.appendChild(h3);

      const container = document.createElement("div");
      container.id = "table-of-contents";

      document.body.appendChild(content);
      document.body.appendChild(container);

      generateTableOfContents(content, container);

      expect(h2a.id).toBe("first-section");
      expect(h2b.id).toBe("second-section");
      expect(h3.id).toBe("subsection");
    });

    it.each([
      ["h2", "Level 2", "0rem"],
      ["h3", "Level 3", "1rem"],
      ["h4", "Level 4", "2rem"],
    ])("should set correct margin-left based on heading level (%s)", (tag, text, expectedMargin) => {
      const content = document.createElement("div");
      content.className = "page-content";

      const heading = document.createElement(tag);
      heading.innerText = text;
      content.appendChild(heading);

      const container = document.createElement("div");
      container.id = "table-of-contents";

      document.body.appendChild(content);
      document.body.appendChild(container);

      generateTableOfContents(content, container);

      const listItem = container.querySelector(".p-table-of-contents__item");
      expect(listItem.style.marginLeft).toBe(expectedMargin);
    });

    it("should create anchor elements with correct href and text", () => {
      const content = document.createElement("div");
      content.className = "page-content";

      const h2 = document.createElement("h2");
      h2.innerText = "About Us";
      content.appendChild(h2);

      const container = document.createElement("div");
      container.id = "table-of-contents";

      document.body.appendChild(content);
      document.body.appendChild(container);

      generateTableOfContents(content, container);

      const anchor = container.querySelector(".p-table-of-contents__link");
      expect(anchor.href).toContain("#about-us");
      expect(anchor.innerText).toBe("About Us");
    });

    it("should scroll to heading if URL hash matches", () => {
      const content = document.createElement("div");
      content.className = "page-content";

      const h2 = document.createElement("h2");
      h2.innerText = "Target Section";
      content.appendChild(h2);

      const container = document.createElement("div");
      container.id = "table-of-contents";

      document.body.appendChild(content);
      document.body.appendChild(container);

      // Mock scrollIntoView
      const scrollSpy = jest.fn();
      h2.scrollIntoView = scrollSpy;

      // Set URL hash
      window.location.hash = "#target-section";

      generateTableOfContents(content, container);

      expect(scrollSpy).toHaveBeenCalled();
    });

    it("should not scroll to heading if URL hash does not match", () => {
      const content = document.createElement("div");
      content.className = "page-content";

      const h2 = document.createElement("h2");
      h2.innerText = "Target Section";
      const scrollSpy = jest.fn();
      h2.scrollIntoView = scrollSpy;

      content.appendChild(h2);

      const container = document.createElement("div");
      container.id = "table-of-contents";

      document.body.appendChild(content);
      document.body.appendChild(container);

      // Set URL hash to something else
      window.location.hash = "#different-section";

      generateTableOfContents(content, container);

      expect(scrollSpy).not.toHaveBeenCalled();
    });

    it("should prepend list to container", () => {
      const content = document.createElement("div");
      content.className = "page-content";

      const h2 = document.createElement("h2");
      h2.innerText = "Section";
      content.appendChild(h2);

      const container = document.createElement("div");
      container.id = "table-of-contents";
      const existingContent = document.createElement("p");
      existingContent.innerText = "Existing content";
      container.appendChild(existingContent);

      document.body.appendChild(content);
      document.body.appendChild(container);

      generateTableOfContents(content, container);

      // List should be the first child
      const list = container.querySelector(".p-table-of-contents__list");
      expect(container.firstChild).toBe(list);
      expect(list.nextSibling).toBe(existingContent);
    });

    it("should handle multiple headings in correct order", () => {
      const content = document.createElement("div");
      content.className = "page-content";

      const headings = ["Introduction", "Features", "Pricing", "Contact"];
      headings.forEach((text) => {
        const h2 = document.createElement("h2");
        h2.innerText = text;
        content.appendChild(h2);
      });

      const container = document.createElement("div");
      container.id = "table-of-contents";

      document.body.appendChild(content);
      document.body.appendChild(container);

      generateTableOfContents(content, container);

      const anchors = container.querySelectorAll(".p-table-of-contents__link");
      expect(anchors.length).toBe(4);
      expect(anchors[0].innerText).toBe("Introduction");
      expect(anchors[1].innerText).toBe("Features");
      expect(anchors[2].innerText).toBe("Pricing");
      expect(anchors[3].innerText).toBe("Contact");
    });

    it("should handle headings with special characters in text", () => {
      const content = document.createElement("div");
      content.className = "page-content";

      const h2 = document.createElement("h2");
      h2.innerText = "API Reference. Guide.";
      content.appendChild(h2);

      const container = document.createElement("div");
      container.id = "table-of-contents";

      document.body.appendChild(content);
      document.body.appendChild(container);

      generateTableOfContents(content, container);

      expect(h2.id).toBe("api-reference-guide");
    });

    it("should handle headings with numbers", () => {
      const content = document.createElement("div");
      content.className = "page-content";

      const h2 = document.createElement("h2");
      h2.innerText = "Step 1: Getting Started";
      content.appendChild(h2);

      const container = document.createElement("div");
      container.id = "table-of-contents";

      document.body.appendChild(content);
      document.body.appendChild(container);

      generateTableOfContents(content, container);

      expect(h2.id).toBe("step-1-getting-started");
    });
  });
});

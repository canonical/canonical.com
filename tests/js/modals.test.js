/** @jest-environment jsdom */

const MODAL_ID = "test-modal";

function renderPage() {
  document.body.innerHTML = `
    <a class="js-invoke-modal" href="/contact-us" aria-controls="${MODAL_ID}">
      <h4>Tell us more about your needs</h4>
    </a>
    <div class="p-modal" id="${MODAL_ID}" style="display: none">
      <div class="p-modal__dialog js-modal-content">
        <button class="p-modal-close-button" aria-controls="${MODAL_ID}">
          <span>Close</span>
        </button>
      </div>
    </div>
  `;
}

function modalDisplay() {
  return document.getElementById(MODAL_ID).style.display;
}

describe("modal click handling", () => {
  beforeAll(() => {
    renderPage();
    require("../../static/js/modals.js");
  });

  beforeEach(() => {
    renderPage();
  });

  it("opens and closes the modal when the trigger elements are clicked", () => {
    document.querySelector(".js-invoke-modal").click();
    expect(modalDisplay()).toBe("flex");

    document.querySelector(".p-modal-close-button").click();
    expect(modalDisplay()).toBe("none");
  });

  it("opens the modal when the click lands on a child of the trigger", () => {
    document.querySelector(".js-invoke-modal h4").click();
    expect(modalDisplay()).toBe("flex");

    document.querySelector(".p-modal-close-button").click();
    expect(modalDisplay()).toBe("none");
  });

  it("closes the modal when the click lands on a child of the close button", () => {
    document.querySelector(".js-invoke-modal").click();
    expect(modalDisplay()).toBe("flex");

    document.querySelector(".p-modal-close-button span").click();
    expect(modalDisplay()).toBe("none");
  });
});

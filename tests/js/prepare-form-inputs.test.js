/** @jest-environment jsdom */

jest.mock("intl-tel-input", () =>
  jest.fn().mockReturnValue({ isValidNumber: jest.fn() })
);

import { setupIntlTelInput } from "../../static/js/prepare-form-inputs.js";

// Fields that intlTelInput is allowed to submit as hidden inputs.
// Matches ALLOWED_HIDDEN_FIELDS in tests/helpers.py.
const ALLOWED_HIDDEN_FIELDS = new Set(["phone"]);

describe("setupIntlTelInput", () => {
  let intlTelInput;

  beforeEach(() => {
    intlTelInput = jest.requireMock("intl-tel-input");
    intlTelInput.mockClear();
    // addInputValidation calls document.querySelector(".iti") and needs a parent
    document.body.innerHTML = '<div><div class="iti"></div></div>';
  });

  it("hiddenInput callback only returns allowed field names", () => {
    const phoneInput = document.createElement("input");
    phoneInput.type = "tel";
    phoneInput.name = "phone";
    document.body.appendChild(phoneInput);

    setupIntlTelInput("gb", phoneInput);

    const config = intlTelInput.mock.calls[0][1];
    const hiddenFields = config.hiddenInput();

    Object.keys(hiddenFields).forEach((key) => {
      expect(ALLOWED_HIDDEN_FIELDS.has(key)).toBe(true);
    });
  });
});

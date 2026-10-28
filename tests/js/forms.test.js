/** @jest-environment jsdom */

jest.mock("../../static/js/prepare-form-inputs", () => ({
  prepareInputFields: jest.fn(),
}));

describe("form submission cookie fields", () => {
  let form;

  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <form action="https://ubuntu.com/marketo/submit" method="post">
        <input type="hidden" name="formid" value="1234">
        <input type="radio" name="_radio_interest" value="cloud" checked>
        <input type="checkbox" name="_checkbox_interest" value="support" checked>
        <button type="submit">Submit</button>
      </form>
    `;
    form = document.querySelector("form");
    require("../../static/js/forms");
  });

  afterEach(() => {
    document.cookie.split(";").forEach((cookie) => {
      const name = cookie.split("=")[0].trim();
      document.cookie = `${name}=;max-age=0;path=/`;
    });
    document.body.innerHTML = "";
  });

  function submitForm() {
    form.dispatchEvent(
      new Event("submit", { bubbles: true, cancelable: true })
    );
    return new FormData(form);
  }

  it.each(["all", "performance", "functionality", "essential", "unset"])(
    "submits the current %s consent value as a hidden field",
    (consent) => {
      document.cookie = `_cookies_accepted=${consent};path=/`;

      const data = submitForm();

      expect(data.getAll("_cookies_accepted")).toEqual([consent]);
      expect(form.querySelector('[name="_cookies_accepted"]').type).toBe(
        "hidden"
      );
      expect(data.has("_radio_interest")).toBe(false);
      expect(data.has("_checkbox_interest")).toBe(false);
      expect(data.get("formid")).toBe("1234");
    }
  );

  it("does not invent consent when the cookie is absent", () => {
    expect(submitForm().has("_cookies_accepted")).toBe(false);
  });

  it("reads consent at submission time rather than initialization", () => {
    document.cookie = "_cookies_accepted=all;path=/";
    submitForm();

    document.cookie = "_cookies_accepted=essential;path=/";

    expect(submitForm().getAll("_cookies_accepted")).toEqual(["essential"]);
  });

  it("preserves the existing cookie fields", () => {
    const cookies = {
      user_id: "visitor-id",
      consent_info: '{"analytics_storage":"granted"}',
      utms: "utm_source%3Atest%26utm_medium%3Aemail",
    };
    Object.entries(cookies).forEach(([name, value]) => {
      document.cookie = `${name}=${value};path=/`;
    });
    document.cookie = "_cookies_accepted=all;path=/";

    const data = submitForm();

    Object.entries(cookies).forEach(([name, value]) => {
      expect(data.get(name)).toBe(value);
    });
  });
});

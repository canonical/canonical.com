import { Page } from "@playwright/test";

export const isExistingField = async (page, fieldName) => {
  const field = page.locator(fieldName);
  return await field.isVisible();
};

export const acceptCookiePolicy = async (
  page: Page,
) => {
  if (await isExistingField(page, '#cookie-policy-button-accept')) {
    await page.locator('#cookie-policy-button-accept').click();
  }
};

/**
 * Fills existing fields in the form
 * @param page Current page
 * @param testTextFields List of text fields to fill
 * @param testCheckboxFields List of checkbox fields to fill
 * @param testRadioFields List of radio fields to fill
 */
export const fillExistingFields = async (page, testTextFields, testCheckboxFields, testRadioFields) => {
  for (const { field, value } of testTextFields) {
    if (await isExistingField(page, field)) {
      await page.fill(field, value);
    }
  }
  for (const { field, value } of testCheckboxFields) {
    if (await isExistingField(page, field)) {
      await page.locator(field).check({ force: true });
    }
  }
  for (const { field, value } of testRadioFields) {
    if (await isExistingField(page, field)) {
      await page.locator(field).click({ force: true });
    }
  }
};

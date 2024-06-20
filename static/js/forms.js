import { prepareInputFields } from "./prepare-form-inputs";

/**
 *
 * @param {Node} submitButton
 *
 * Attaches a loading spinner to the submit button on
 * form submission
 */
function attachLoadingSpinner(submitButton) {
  const spinnerIcon = document.createElement("i");
  spinnerIcon.className = "p-icon--spinner u-animation--spin is-light";
  const buttonRect = submitButton.getBoundingClientRect();
  submitButton.style.width = buttonRect.width + "px";
  submitButton.style.height = buttonRect.height + "px";
  submitButton.classList.add("is-processing");
  submitButton.disabled = true;
  submitButton.innerText = "";
  submitButton.appendChild(spinnerIcon);
}
const form = document.querySelector("form");
const submitButton = form.querySelector('button[type="submit"]');
// Exclude forms that don't need loader
const cancelLoader = submitButton.classList.contains("no-loader");
if (submitButton && !cancelLoader) {
  form.addEventListener("submit", () => attachLoadingSpinner(submitButton));
}

// This block checks for the presence of 'phone number' and 'country' input fields on the page. If either input field exists, it triggers the `prepareInputFields` function to set them up. Note: In a modal form scenario, these inputs are not present at page load and thus, `prepareInputFields` is not invoked here. Instead, the function is imported and executed within `dynamic-forms.js` when the modal is opened.
const phoneNumberInput = document.querySelector("input#phone");
const countryInput = document.querySelector("select#country");
if (phoneNumberInput || countryInput) {
  prepareInputFields(phoneNumberInput, countryInput);
}

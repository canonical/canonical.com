import { prepareInputFields } from "./prepare-form-inputs.js";

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

const phoneNumberInput = document.querySelector("input#phone");
const countryInput = document.querySelector("select#country");
prepareInputFields(phoneNumberInput, countryInput);

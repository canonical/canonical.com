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

/**
 *
 * @param {*} fieldset
 * @param {*} checklistItem
 *
 * Disable & enable checklist visibility based on user selection
 * - When any visible checkbox is checked, it will disable the .js-checkbox-visibility__other checkboxes
 * - Can only check one __other item at a time
 * - When all visible checkboxes or any __other checkbox is unchecked, all checkboxes will be enabled
 */
function toggleCheckboxVisibility(fieldset, checklistItem) {
  const checkboxes = fieldset.querySelectorAll(".js-checkbox-visibility");
  const otherCheckboxes = fieldset.querySelectorAll(
    ".js-checkbox-visibility__other",
  );
  const isVisible = checklistItem.classList.contains(
    "js-checkbox-visibility",
  );

  if (checklistItem.checked) {
    if (isVisible) {
      otherCheckboxes.forEach((checkbox) => {
        checkbox.disabled = true;
      });
    } else {
      checkboxes.forEach((checkbox) => {
        checkbox.disabled = true;
      });
      otherCheckboxes.forEach((checkbox) => {
        checklistItem == checkbox ? null : (checkbox.disabled = true);
      });
    }
  } else {
    if (isVisible) {
      var uncheck = true;
      checkboxes.forEach((checkbox) => {
        checkbox.checked ? (uncheck = false) : null;
      });
      if (uncheck) {
        otherCheckboxes.forEach((checkbox) => {
          checkbox.disabled = false;
        });
      }
    } else {
      checkboxes.forEach((checkbox) => {
        checkbox.disabled = false;
      });
      otherCheckboxes.forEach((checkbox) => {
        checkbox.disabled = false;
      });
    }
  }
}

/**
 *
 * @param {*} fieldset
 * @param {*} target
 * Disables submit button for required checkboxes field
 */
function requiredCheckbox(fieldset, target) {
  const submitButton = document.querySelector(".js-submit-button");
  const checkboxes = fieldset.querySelectorAll("input[type='checkbox']");
  if (target.checked) {
    submitButton.disabled = false;
  } else {
    var disableSubmit = true;
    checkboxes.forEach((checkbox) => {
      checkbox.checked ? (disableSubmit = false) : null;
    });
    submitButton.disabled = disableSubmit;
  }
}
// Add event listeners to toggle checkbox visibility
const ubuntuVersionCheckboxes = document.querySelector(
  "fieldset.js-toggle-checkbox-visibility",
);
ubuntuVersionCheckboxes?.addEventListener("change", function (event) {
  toggleCheckboxVisibility(ubuntuVersionCheckboxes, event.target);
});

// Add event listeners to required fieldset
const requiredFieldset = document.querySelectorAll(
  "fieldset.js-required-checkbox",
);

const form = document.querySelector("form");
const submitButton = form.querySelector('button[type="submit"]');
if(requiredFieldset) submitButton.disabled = true;

requiredFieldset?.forEach((fieldset) => {
  fieldset.addEventListener("change", function (event) {
    requiredCheckbox(fieldset, event.target);
  });
});

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

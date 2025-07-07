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
    ".js-checkbox-visibility__other"
  );
  const isVisible = checklistItem.classList.contains("js-checkbox-visibility");

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

/**
 * Sets the consent info from the data layer into the consent_info cookie
 */
function setDataLayerConsentInfo() {
  const dataLayer = window.dataLayer || [];
  const latestConsentUpdateElements = dataLayer
    .slice()
    .reverse()
    .filter(
      (item) =>
        typeof item === "object" &&
        item !== null &&
        item[0] === "consent" &&
        item[1] === "update",
    )[0]?.[2];

  if (latestConsentUpdateElements) {
    document.cookie =
      "consent_info=" +
      JSON.stringify(latestConsentUpdateElements) +
      ";max-age=31536000;";
  }
}

function getCookie(name) {
  const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
  return match ? match[2] : null;
}

/**
 * Adds cookie values as hidden form fields
 */
function addCookieFieldsToForm(form) {
  const cookieFields = ['user_id', 'consent_info', 'utms'];
  
  cookieFields.forEach(fieldName => {
    const cookieValue = getCookie(fieldName);
    if (cookieValue) {
      // Remove existing hidden field if it exists
      const existingField = form.querySelector(`input[name="${fieldName}"]`);
      if (existingField) {
        existingField.remove();
      }
      
      // Create new hidden field
      const hiddenField = document.createElement('input');
      hiddenField.type = 'hidden';
      hiddenField.name = fieldName;
      hiddenField.value = cookieValue;
      form.appendChild(hiddenField);
      
      console.log(`Added ${fieldName} to form:`, cookieValue);
    }
  });
}

const forms = document.querySelectorAll("form");
forms.forEach((form) => {
  // Add event listeners to toggle checkbox visibility
  const ubuntuVersionCheckboxes = document.querySelector(
    "fieldset.js-toggle-checkbox-visibility"
  );
  ubuntuVersionCheckboxes?.addEventListener("change", function (event) {
    toggleCheckboxVisibility(ubuntuVersionCheckboxes, event.target);
  });

  const submitButton = form.querySelector('button[type="submit"]');
  const requiredFieldset = form.querySelectorAll(
    "fieldset.js-required-checkbox"
  );
  // By default we disable the button, until the required fields are selected
  if (requiredFieldset.length) submitButton.disabled = true;

  // Add event listeners to required fieldset
  requiredFieldset?.forEach((fieldset) => {
    fieldset.addEventListener("change", function (event) {
      requiredCheckbox(fieldset, event.target);
    });
  });

  // Exclude forms that don't need loader
  const cancelLoader = submitButton?.classList.contains("no-loader");
  if (submitButton && !cancelLoader) {
    form.addEventListener("submit", () => {
      attachLoadingSpinner(submitButton);
      setDataLayerConsentInfo();
      addCookieFieldsToForm(form);
    });
  }

  // This block checks for the presence of 'phone number' and 'country' input fields on the page. If either input field exists, it triggers the `prepareInputFields` function to set them up. Note: In a modal form scenario, these inputs are not present at page load and thus, `prepareInputFields` is not invoked here. Instead, the function is imported and executed within `dynamic-forms.js` when the modal is opened.
  const phoneNumberInput = form.querySelector("input#phone");
  const countryInput = form.querySelector("select#country");
  if (phoneNumberInput || countryInput) {
    prepareInputFields(phoneNumberInput, countryInput);
  }
});

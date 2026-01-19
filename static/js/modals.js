(function () {
  var currentDialog = null;
  var lastFocus = null;
  var ignoreFocusChanges = false;
  var focusAfterClose = null;
  var modalTrigger = null;

  const triggeringHash = "#get-in-touch";

  // Removes the triggering hash
  function updateHash(hash) {
    var location = window.location;
    if (location.hash !== hash || hash === "") {
      if ("pushState" in history) {
        history.pushState(
          "",
          document.title,
          location.pathname + location.search + hash
        );
      } else {
        location.hash = hash;
      }
    }
  }

  // Opens the form when the initial hash matches the trigger
  if (window.location.hash === triggeringHash) {
    toggleModal(document.querySelector(".p-modal"), null, true);
  }

  // Listens for hash changes and opens the form if it matches the trigger
  function locationHashChanged() {
    if (window.location.hash === triggeringHash) {
      toggleModal(document.querySelector(".p-modal"), null, true);
    }
  }
  window.onhashchange = locationHashChanged;

  // Traps the focus within the currently open modal dialog
  function trapFocus(event) {
    if (ignoreFocusChanges) return;

    if (currentDialog.contains(event.target)) {
      lastFocus = event.target;
    } else {
      focusFirstDescendant(currentDialog);
      if (lastFocus == document.activeElement) {
        focusLastDescendant(currentDialog);
      }
      lastFocus = document.activeElement;
    }
  }

  // Attempts to focus given element
  function attemptFocus(child) {
    if (child.focus) {
      ignoreFocusChanges = true;
      child.focus();
      ignoreFocusChanges = false;
      return document.activeElement === child;
    }

    return false;
  }

  // Focuses first child element
  function focusFirstDescendant(element) {
    for (var i = 0; i < element.childNodes.length; i++) {
      var child = element.childNodes[i];
      if (attemptFocus(child) || focusFirstDescendant(child)) {
        return true;
      }
    }
    return false;
  }

  // Focuses last child element
  function focusLastDescendant(element) {
    for (var i = element.childNodes.length - 1; i >= 0; i--) {
      var child = element.childNodes[i];
      if (attemptFocus(child) || focusLastDescendant(child)) {
        return true;
      }
    }
    return false;
  }

  // Handle click outside modal
  function handleModalClick(e) {
    if (!e.target.closest(".js-modal-content")) {
      closeModals();
    }
  }

  /**
    Toggles visibility of modal dialog.
    @param {HTMLElement} modal Modal dialog to show or hide.
    @param {HTMLElement} sourceEl Element that triggered toggling modal
    @param {Boolean} open If defined as `true` modal will be opened, if `false` modal will be closed, undefined toggles current visibility.
  */
  function toggleModal(modal, sourceEl, open) {
    if (modal && modal.classList.contains("p-modal")) {
      if (typeof open === "undefined") {
        open = modal.style.display === "none";
      }

      if (open) {
        document.body.style.overflow = "hidden";
        currentDialog = modal;
        modal.style.display = "flex";
        focusAfterClose = sourceEl;
        document.addEventListener("focus", trapFocus, true);
        document.addEventListener("click", handleModalClick);
        updateHash(triggeringHash);
      } else {
        document.body.style.overflow = "auto";
        modal.style.display = "none";
        if (focusAfterClose && focusAfterClose.focus) {
          focusAfterClose.focus();
        }
        document.removeEventListener("focus", trapFocus, true);
        document.removeEventListener("click", handleModalClick);
        updateHash("");
        currentDialog = null;
      }
    }
  }

  // Find and hide all modals on the page
  function closeModals() {
    var modals = [].slice.apply(document.querySelectorAll(".p-modal"));
    setState(1);
    modals.forEach(function (modal) {
      toggleModal(modal, false, false);
    });
    if (modalTrigger) {
      modalTrigger.setAttribute("aria-expanded", false);
    }
  }

  // Add click handler for clicks on elements with aria-controls
  document.addEventListener("click", function (e) {
    const isModalTrigger = e.target.closest(".js-invoke-modal");
    const isCloseButton = e.target.closest(".p-modal-close-button");
    if (isModalTrigger) modalTrigger = isModalTrigger;
    if (isModalTrigger || isCloseButton) {
      e.preventDefault();

      const targetControls = e.target.getAttribute("aria-controls");
      const toggleValue = Boolean(isModalTrigger);
      toggleModal(
        document.getElementById(targetControls),
        e.target,
        toggleValue
      );

      if (modalTrigger) {
        modalTrigger.setAttribute("aria-expanded", toggleValue);
      }
    }
    return false;
  });

  // Handle Pagination
  let contactIndex = 1;
  const contactModal = document.querySelector(".p-modal");
  const modalPaginationButtons = contactModal.querySelectorAll(".pagination a");
  const paginationContent = contactModal.querySelectorAll(".js-pagination");

  function setState(index) {
    contactIndex = index;
    render();
  }

  function render() {
    if (paginationContent.length) {
      const currentContent = contactModal.querySelector(
        ".js-pagination--" + contactIndex
      );
      paginationContent.forEach(function (content) {
        content.classList.add("u-hide");
      });
      currentContent.classList.remove("u-hide");
    }
  }

  modalPaginationButtons.forEach(function (modalPaginationButton) {
    modalPaginationButton.addEventListener("click", function (e) {
      e.preventDefault();
      const button = e.target.closest("a");
      let index = contactIndex;
      if (button.classList.contains("pagination__link--previous")) {
        index = index - 1;
        setState(index);
        dataLayer.push({
          event: "interactive-forms",
          action: "goto:" + index,
          path: window.location.pathname,
        });
      } else {
        index = index + 1;
        setState(index);
        dataLayer.push({
          event: "interactive-forms",
          action: "goto:" + index,
          path: window.location.pathname,
        });
      }
    });
  });

  // Add handler for closing modals using ESC key.
  document.addEventListener("keydown", function (e) {
    e = e || window.event;

    if (e.code === "Escape") {
      closeModals();
    } else if (e.keyCode === 27) {
      closeModals();
    }
  });
})();

function validateCheckbox(event, fieldsetId) {
  const checkboxes = Array.from(
    document
      .getElementById(fieldsetId)
      .querySelectorAll("input[class='p-checkbox__input']")
  );
  if (event.currentTarget.checked) {
    checkboxes[0].removeAttribute("required");
  }
}

function getCustomFields(event) {
  var message = "";
  var formFields = document.querySelectorAll(".js-formfield");

  formFields.forEach(function (formField) {
    // Only include form fields in the message payload that have the class js-formfield
    const includeFormField = formField.querySelector(".js-formfield");
    var comma = ",";
    var fieldsetForm = formField.querySelector(".js-formfield-title");
    var fieldTitle = "";
    if (fieldsetForm) {
      fieldTitle = fieldsetForm;
    } else {
      fieldTitle =
        formField.querySelector(".p-heading--5") ??
        formField.querySelector(".p-modal__question-heading");
    }
    var inputs = formField.querySelectorAll(
      "input, textarea:not(.js-other-input), select"
    );
    if (fieldTitle) {
      message += fieldTitle.innerText + "\r\n";
    }

    inputs.forEach(function (input) {
      switch (input.type) {
        case "select-one":
          message +=
            input.options[input.selectedIndex]?.textContent + comma + " ";
          break;
        case "radio":
          if (input.checked) {
            message += input.value + comma + " ";
          }
          break;
        case "checkbox":
          if (input.checked) {
            if (fieldsetForm) {
              message += input.value + comma + " ";
            } else {
              // Forms that have column separation
              var subSectionText = "";
              if (
                input.closest('[class*="col-"]') &&
                input
                  .closest('[class*="col-"]')
                  .querySelector(".js-sub-section")
              ) {
                var subSection = input
                  .closest('[class*="col-"]')
                  .querySelector(".js-sub-section");
                subSectionText = subSection.innerText + ": ";
              }

              var label = formField.querySelector(
                "span#" + input.getAttribute("aria-labelledby")
              );

              if (label) {
                label = subSectionText + label.innerText;
              } else {
                label = input.getAttribute("aria-labelledby");
              }
              message += label + comma + "\r\n\r\n";
            }
          }
          break;
        case "text":
        case "number":
        case "textarea":
          if (
            input.value !== "" &&
            !input.classList.contains("js-other-input")
          ) {
            message += input.value + comma + " ";
          }
          break;
      }
    });
    message += "\r\n\r\n";
  });

  const radioFieldsets = document.querySelectorAll(".js-remove-radio-names");
  if (radioFieldsets.length > 0) {
    radioFieldsets.forEach((radioFieldset) => {
      const radioInputs = radioFieldset.querySelectorAll("input[type='radio']");
      radioInputs.forEach((radioInput) => {
        radioInput.removeAttribute("name");
      });
    });
  }

  const checkboxFieldsets = document.querySelectorAll(
    ".js-remove-checkbox-names"
  );
  if (checkboxFieldsets.length > 0) {
    checkboxFieldsets.forEach((checkboxFieldset) => {
      const checkboxInputs = checkboxFieldset.querySelectorAll(
        "input[type='checkbox']"
      );
      checkboxInputs.forEach((checkboxInput) => {
        checkboxInput.removeAttribute("name");
      });
    });
  }

  const textarea = document.getElementById("Comments_from_lead__c");
  textarea.value = message;
}

(function () {
  var currentDialog = null;
  var lastFocus = null;
  var ignoreFocusChanges = false;
  var focusAfterClose = null;

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
        document.body.style.overflow = 'hidden';
        currentDialog = modal;
        modal.style.display = "flex";
        focusAfterClose = sourceEl;
        document.addEventListener("focus", trapFocus, true);
        updateHash(triggeringHash);
      } else {
        document.body.style.overflow = 'auto';
        modal.style.display = "none";
        if (focusAfterClose && focusAfterClose.focus) {
          focusAfterClose.focus();
        }
        document.removeEventListener("focus", trapFocus, true);
        updateHash("");
        currentDialog = null;
      }
    }
  }

  // Find and hide all modals on the page
  function closeModals() {
    var modals = [].slice.apply(document.querySelectorAll(".p-modal"));
    modals.forEach(function (modal) {
      toggleModal(modal, false, false);
    });
  }

  // Add click handler for clicks on elements with aria-controls
  document.addEventListener("click", function (event) {
    var targetControls = event.target.getAttribute("aria-controls");
    if (targetControls) {
      event.preventDefault();

      toggleModal(document.getElementById(targetControls), event.target);
    }

    return false;
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

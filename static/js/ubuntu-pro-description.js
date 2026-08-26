/**
 * Ubuntu Pro Description — page-level JS
 *
 * Wires up the export-pdf modal and handles the Export and Select-all
 * button actions. Loaded synchronously after modal.js so that initModals
 * is already defined when this script runs.
 */

// Initialise the export-pdf modal (from static/js/src/modal.js).
initModals("#export-pdf-modal", "[aria-controls=export-pdf-modal]", false);

// Return the non-disabled section checkboxes in the modal.
function getSectionCheckboxes() {
  return Array.prototype.slice.call(
    document.querySelectorAll(
      '#export-pdf-modal input[name="section"]:not([disabled])',
    ),
  );
}

// Return true when every non-disabled section checkbox is checked.
function allSectionsSelected() {
  return getSectionCheckboxes().every(function (cb) {
    return cb.checked;
  });
}

// Keep the Select-all / Clear-all link label in sync with checkbox state.
function updateSelectAllLabel() {
  var link = document.querySelector(".js-select-all");
  if (link) {
    link.textContent = allSectionsSelected() ? "Clear all" : "Select all";
  }
}

// Update label whenever a section checkbox changes.
document
  .querySelectorAll('#export-pdf-modal input[name="section"]')
  .forEach(function (cb) {
    cb.addEventListener("change", updateSelectAllLabel);
  });

// Set initial label state.
updateSelectAllLabel();

document.addEventListener("click", function (e) {
  var target = e.target;

  // Export button: open the print view in a new tab. The print page
  // re-renders the selected sections from source, making the export
  // tamper-proof regardless of DOM changes on the main page.
  if (target.classList.contains("js-export-pdf")) {
    var checked = Array.prototype.slice
      .call(
        document.querySelectorAll(
          '#export-pdf-modal input[name="section"]:checked',
        ),
      )
      .map(function (cb) {
        return cb.value;
      });
    if (checked.length === 0) return;
    window.open(
      "/legal/ubuntu-pro-description/print?sections=" +
        checked.map(encodeURIComponent).join(","),
      "_blank",
      "noopener,noreferrer",
    );
    return;
  }

  // Select-all / Clear-all link: toggle all non-disabled checkboxes.
  if (target.classList.contains("js-select-all")) {
    e.preventDefault();
    var selectAll = !allSectionsSelected();
    getSectionCheckboxes().forEach(function (cb) {
      cb.checked = selectAll;
    });
    updateSelectAllLabel();
  }
});

// Definition back-link: show a "Back to main content" button directly after
// the definition paragraph that the user navigated to via a #def-* anchor.
// Clicking it calls history.back() to return to the link that was clicked.
(function () {
  var btn = null;

  function removeButton() {
    if (btn && btn.parentNode) {
      btn.parentNode.removeChild(btn);
    }
  }

  function placeButton() {
    removeButton();

    var hash = window.location.hash;
    if (!hash || !hash.startsWith("#def-")) return;

    var target = document.getElementById(hash.slice(1));
    if (!target) return;

    // Each definition term lives inside a <p>; insert the button after it.
    var para = target.closest("p");
    if (!para || !para.parentNode) return;

    if (!btn) {
      btn = document.createElement("button");
      btn.className = "p-button js-def-back-btn";
      btn.textContent = "Back to main content";
      btn.addEventListener("click", function () {
        history.back();
      });
    }

    // Insert before the paragraph so the float sits to its right while
    // the definition text flows alongside it on the left.
    para.parentNode.insertBefore(btn, para);
  }

  window.addEventListener("hashchange", placeButton);
  placeButton();
})();

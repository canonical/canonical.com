/**
 * Ubuntu Pro Description — page-level JS
 *
 * Wires up the export-pdf modal and handles the Export and Select-all
 * button actions. Loaded synchronously after modal.js so that initModals
 * is already defined when this script runs.
 */

// Initialise the export-pdf modal (from static/js/src/modal.js).
initModals("#export-pdf-modal", "[aria-controls=export-pdf-modal]", false);

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
      "/legal/ubuntu-pro-description/print?sections=" + checked.join(","),
      "_blank",
      "noopener,noreferrer",
    );
    return;
  }

  // Select-all link: check every section checkbox.
  if (target.classList.contains("js-select-all")) {
    e.preventDefault();
    document
      .querySelectorAll('#export-pdf-modal input[name="section"]')
      .forEach(function (cb) {
        cb.checked = true;
      });
  }
});

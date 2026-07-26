/**
 * Ubuntu Pro Description — print view JS
 *
 * Triggers the browser print dialog on load and closes the tab after the
 * user dismisses it. Loaded by _print.html only.
 *
 * afterprint is registered BEFORE calling print() so the handler is always
 * in place. Using afterprint rather than calling close() immediately after
 * print() prevents the tab from closing before the dialog appears — window.print
 * is not guaranteed to be synchronous in all browsers.
 */
window.addEventListener("load", function () {
  window.addEventListener("afterprint", function () {
    window.close();
  });
  window.print();
});

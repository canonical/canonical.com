(function () {
  function hasConsent() {
    var match = document.cookie.match(
      /(?:^|;\s*)_cookies_accepted=([^;]+)/
    );
    return match && (match[1] === "all" || match[1] === "performance");
  }

  function loadUsabilla() {
    if (window.usabilla_live || window.__usabilla_loaded) return;
    window.__usabilla_loaded = true;
    var script = document.createElement("script");
    script.src = "https://w.usabilla.com/ecdf1756070a.js?lv=1";
    script.async = true;
    document.head.appendChild(script);
  }

  if (hasConsent()) {
    loadUsabilla();
  }

  if (window.cookieStore && window.cookieStore.addEventListener) {
    window.cookieStore.addEventListener("change", function (event) {
      var changed = (event.changed || []).some(function (cookie) {
        return cookie.name === "_cookies_accepted";
      });
      if (changed && hasConsent()) {
        loadUsabilla();
      }
    });
  }
})();

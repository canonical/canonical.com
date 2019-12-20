function initTabs() {
  var tabLinks = document.querySelectorAll("a[href^='#']");

  // prevent the page jumping around when switching tabs,
  // whilst still using :target
  // https://gist.github.com/pimterry/260841c2104f27cadc954a29b9873b96#file-disable-link-jump-with-workaround-js
  [].forEach.call(tabLinks, function (link) {
    link.addEventListener("click", function (event) {
      event.preventDefault();
      history.pushState({}, "", link.href);
      
      // Update the URL again with the same hash, then go back
      history.pushState({}, "", link.href);
      history.back();

      setActiveTab();
    });
  });

  document.addEventListener("DOMContentLoaded", setActiveTab());

  window.onhashchange = function() { 
    setActiveTab();
  }

  function setActiveTab() {
    var urlHash = window.location.hash;
    [].forEach.call(tabLinks, function (link) {
      if (urlHash) {
        if ("#" + link.getAttribute("aria-controls") === urlHash) {
          link.setAttribute("aria-selected", true);
        } else {
          link.setAttribute("aria-selected", false);
        }
      }
    });
  };
}

initTabs();

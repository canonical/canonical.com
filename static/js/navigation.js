  var nav = document.getElementById("navigation");
  var navDropdowns = document.querySelectorAll(
    ".p-navigation__item--dropdown-toggle:not(.is-selected)"
  );
  var dropdownWindow = document.querySelector(".dropdown-window");
  var dropdownWindowOverlay = document.querySelector(
    ".dropdown-window-overlay"
  );

  navDropdowns.forEach(function (dropdown) {
    dropdown.addEventListener("click", function (event) {
      event.preventDefault();

      var clickedDropdown = this;

      dropdownWindow.style.height = 
        window.innerHeight - nav.offsetHeight + "px";
      dropdownWindow.classList.remove("slide-animation");
      dropdownWindowOverlay.classList.remove("fade-animation");

      navDropdowns.forEach(function (dropdown) {
        var dropdownContent = document.getElementById(dropdown.id + "-content");

        if (dropdown === clickedDropdown) {
          if (dropdown.classList.contains("is-active")) {
            closeMenu(dropdown);
          } else {
            dropdown.classList.add("is-active");
            dropdownContent.classList.remove("u-hide");
          }
        } else {
          dropdown.classList.remove("is-active");
          dropdownContent.classList.add("u-hide");
        }
      });
    });
  });

  // Close the menu if browser back button is clicked
  window.addEventListener("hashchange", function (event) {
    navDropdowns.forEach(function (dropdown) {
      if (dropdown.classList.contains("is-active")) {
        closeMenu(dropdown);
      }
    });
  });

  dropdownWindowOverlay.addEventListener("click", function (event) {
    navDropdowns.forEach(function (dropdown) {
      if (dropdown.classList.contains("is-active")) {
        closeMenu(dropdown);
      }
    });
  });

  function closeMenu(dropdown) {
      console.log(dropdown)
    dropdown.classList.remove("is-active");
    dropdownWindow.classList.add("slide-animation");
    dropdownWindowOverlay.classList.add("fade-animation");

    setTimeout(function () {
      dropdownWindow.style.top = null;
      dropdownWindow.style.height = null;
    }, 500);

    if (window.history.pushState) {
      window.history.pushState(null, null, window.location.href.split("#")[0]);
    }
  }

  if (window.location.hash) {
    var tabId = window.location.hash.split("#")[1];
    var tab = document.getElementById(tabId);
    var tabContent = document.getElementById(tabId + "-content");

    if (tab) {
      setTimeout(function () {
        document.getElementById(tabId).click();
      }, 0);
    }
  }

  function closeMainMenu() {
    var navigationLinks = document.querySelectorAll(
      ".p-navigation__item--dropdown-toggle:not(.is-selected)"
    );

    navigationLinks.forEach(function (navLink) {
      navLink.classList.remove("is-active");
    });

    if (!dropdownWindowOverlay.classList.contains("fade-animation")) {
      dropdownWindowOverlay.classList.add("fade-animation");
    }

    if (!dropdownWindow.classList.contains("slide-animation")) {
      dropdownWindow.classList.add("slide-animation");
    }
  }

  var origin = window.location.href;

  addGANavEvents("#products-nav", "canonical.com-nav-products");
  addGANavEvents("#partners-nav", "canonical.com-nav-partners");
  addGANavEvents("#careers-nav", "canonical.com-nav-careers");

  function addGANavEvents(target, category) {
    var t = document.querySelector(target);
    if (t) {
      t.querySelectorAll("a").forEach(function (a) {
        a.addEventListener("click", function () {
          dataLayer.push({
            event: "GAEvent",
            eventCategory: category,
            eventAction: `from:${origin} to:${a.href}`,
            eventLabel: a.text,
            eventValue: undefined,
          });
        });
      });
    }
  }

  addGAContentEvents("#main-content");

  function addGAContentEvents(target) {
    var t = document.querySelector(target);
    if (t) {
      t.querySelectorAll("a").forEach(function (a) {
        if (a.className.includes("p-button--positive")) {
          var category = "canonical.com-content-cta-0";
        } else if (a.className.includes("p-button")) {
          var category = "canonical.com-content-cta-1";
        } else {
          var category = "canonical.com-content-link";
        }
        if (!a.href.startsWith("#")) {
          a.addEventListener("click", function () {
            dataLayer.push({
              event: "GAEvent",
              eventCategory: category,
              eventAction: `from:${origin} to:${a.href}`,
              eventLabel: a.text,
              eventValue: undefined,
            });
          });
        }
      });
    }
  }


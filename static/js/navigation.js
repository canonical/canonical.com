function toggleDropdown(toggle, open) {
  var parentElement = toggle.parentNode;
  var dropdown = document.getElementById(toggle.getAttribute('aria-controls'));
  dropdown.setAttribute('aria-hidden', !open);

  if (open) {
    parentElement.classList.add('is-active');
  } else {
    parentElement.classList.remove('is-active');
  }
}

function closeAllDropdowns(toggles) {
  toggles.forEach(function (toggle) {
    toggleDropdown(toggle, false);
  });
}

function handleClickOutside(toggles, containerClass) {
  document.addEventListener('click', function (event) {
    var target = event.target;

    if (target.closest) {
      if (!target.closest(containerClass)) {
        closeAllDropdowns(toggles);
      }
    }
  });
}

function initNavDropdowns(containerClass) {
  var toggles = [].slice.call(document.querySelectorAll(containerClass + ' [aria-controls]'));
  handleClickOutside(toggles, containerClass);

  toggles.forEach(function (toggle) {
    toggle.addEventListener('click', function (e) {
      e.preventDefault();

      const shouldOpen = !toggle.parentNode.classList.contains('is-active');
      closeAllDropdowns(toggles);
      toggleDropdown(toggle, shouldOpen);
    });
  });
}

function initDropdowItems(itemClass) {
  if (window.location.pathname != '/') {
  var items = [].slice.call(document.querySelectorAll(itemClass));
    items.forEach(item => {
      if (item.pathname && item.pathname === window.location.pathname) {
        item.classList.add("is-selected");
      } else {
        item.classList.remove("is-selected");
      }
    });
  }
}

initNavDropdowns('.p-navigation__item--dropdown-toggle');
initDropdowItems('.p-navigation__dropdown-item');


// Init GA tracking
addGANavEvents("#products-nav", "canonical.com-nav-products");
addGANavEvents("#company-nav", "canonical.com-nav-company");
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

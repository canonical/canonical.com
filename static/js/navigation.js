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

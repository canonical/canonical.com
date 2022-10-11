function toggleDropdown(toggle, open) {
  var parentElement = toggle.parentNode;
  var dropdown = document.getElementById(toggle.getAttribute('aria-controls'));
  console.log("dropdown = ", dropdown)
  dropdown.setAttribute('aria-hidden', !open);

  if (open) {
    parentElement.classList.add('is-active');
  } else {
    parentElement.classList.remove('is-active');
  }
}

function closeAllDropdowns(toggles) {
  toggles.forEach(function (toggle) {
    console.log("toggle",toggle)
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
  console.log("initing")
  var toggles = [].slice.call(document.querySelectorAll(containerClass + ' [aria-controls]'));
  handleClickOutside(toggles, containerClass);

  toggles.forEach(function (toggle) {
    toggle.addEventListener('click', function (e) {
      e.preventDefault();

      const shouldOpen = !toggle.parentNode.classList.contains('is-active');
      console.log("closing dropdowns")
      closeAllDropdowns(toggles);
      console.log("toggling dropdown")
      toggleDropdown(toggle, shouldOpen);
    });
  });
}

initNavDropdowns('.p-navigation__item--dropdown-toggle')

function initNavigationSearch(element) {
  const searchButtons = element.querySelectorAll('.js-search-button');

  searchButtons.forEach((searchButton) => {
    searchButton.addEventListener('click', toggleSearch);
  });

  const menuButton = element.querySelector('.js-menu-button');
  if (menuButton) {
    menuButton.addEventListener('click', toggleMenu);
  }

  const overlay = element.querySelector('.p-navigation__search-overlay');
  if (overlay) {
    overlay.addEventListener('click', closeAll);
  }

  function toggleMenu(e) {
    e.preventDefault();

    var navigation = e.target.closest('.p-navigation');
    if (navigation.classList.contains('has-menu-open')) {
      closeAll();
    } else {
      closeAll();
      openMenu(e);
    }
  }

  function toggleSearch(e) {
    e.preventDefault();

    var navigation = e.target.closest('.p-navigation');
    if (navigation.classList.contains('has-search-open')) {
      closeAll();
    } else {
      closeAll();
      openSearch(e);
    }
  }

  function openSearch(e) {
    e.preventDefault();
    var navigation = e.target.closest('.p-navigation');
    var nav = navigation.querySelector('.p-navigation__nav');

    var searchInput = navigation.querySelector('.p-search-box__input');
    var buttons = document.querySelectorAll('.js-search-button');

    buttons.forEach((searchButton) => {
      searchButton.setAttribute('aria-pressed', true);
    });

    navigation.classList.add('has-search-open');
    searchInput.focus();
    document.addEventListener('keyup', keyPressHandler);
  }

  function openMenu(e) {
    e.preventDefault();
    var navigation = e.target.closest('.p-navigation');
    var nav = navigation.querySelector('.p-navigation__nav');

    var buttons = document.querySelectorAll('.js-menu-button');

    buttons.forEach((searchButton) => {
      searchButton.setAttribute('aria-pressed', true);
    });

    navigation.classList.add('has-menu-open');
    document.addEventListener('keyup', keyPressHandler);
  }

  function closeSearch() {
    var navigation = document.querySelector('.p-navigation');
    var nav = navigation.querySelector('.p-navigation__nav');

    var banner = document.querySelector('.p-navigation__banner');
    var buttons = document.querySelectorAll('.js-search-button');

    buttons.forEach((searchButton) => {
      searchButton.removeAttribute('aria-pressed');
    });

    navigation.classList.remove('has-search-open');
    document.removeEventListener('keyup', keyPressHandler);
  }

  function closeMenu() {
    var navigation = document.querySelector('.p-navigation');
    var nav = navigation.querySelector('.p-navigation__nav');

    var banner = document.querySelector('.p-navigation__banner');
    var buttons = document.querySelectorAll('.js-menu-button');

    buttons.forEach((searchButton) => {
      searchButton.removeAttribute('aria-pressed');
    });

    navigation.classList.remove('has-menu-open');
    document.removeEventListener('keyup', keyPressHandler);
  }

  function closeAll() {
    closeSearch();
    closeMenu();
  }

  function keyPressHandler(e) {
    if (e.key === 'Escape') {
      closeAll();
    }
  }
}

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

      closeAllDropdowns(toggles);
      toggleDropdown(toggle, true);
    });
  });
}

var navigation = document.querySelector('#navigation');
initNavigationSearch(navigation);
initNavDropdowns('.p-navigation__item--dropdown-toggle')
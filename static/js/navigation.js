var navDropdowns = document.querySelectorAll('.p-navigation__dropdown-link:not(.is-selected)');
var dropdownWindow = document.querySelector('.dropdown-window');
var dropdownWindowOverlay = document.querySelector('.dropdown-window-overlay');

navDropdowns.forEach(function(dropdown) {
  dropdown.addEventListener('click', function(event) {
    event.preventDefault();

    var clickedDropdown = this;

    dropdownWindow.classList.remove('slide-animation');
    dropdownWindowOverlay.classList.remove('fade-animation');

    navDropdowns.forEach(function(dropdown) {
      var dropdownContent = document.getElementById(dropdown.id + "-content");

      if (dropdown === clickedDropdown) {

        if (dropdown.classList.contains('is-open')) {
          closeMenu(dropdown, dropdownContent);
        } else {
          dropdown.classList.add('is-open');
          dropdownContent.classList.remove('u-hide');

          if (window.history.pushState) {
            window.history.pushState(null, null, '#' + dropdown.id);
          }
        }
      } else {
        dropdown.classList.remove('is-open');
        dropdownContent.classList.add('u-hide');
      }
    });
  });
});

// Close the menu if browser back button is clicked
window.addEventListener('hashchange', function(event) {
  navDropdowns.forEach(function (dropdown) {
    const dropdownContent = document.getElementById(dropdown.id + "-content");

    if (dropdown.classList.contains('is-open')) {
      closeMenu(dropdown, dropdownContent);
    }
  });
})

dropdownWindowOverlay.addEventListener('click', function(event) {
  navDropdowns.forEach(function(dropdown) {
    var dropdownContent = document.getElementById(dropdown.id + "-content");

    if (dropdown.classList.contains('is-open')) {
      closeMenu(dropdown, dropdownContent);
    }
  });
});

function closeMenu(dropdown, dropdownContent) {
  dropdown.classList.remove('is-open');
  dropdownWindow.classList.add('slide-animation');
  dropdownWindowOverlay.classList.add('fade-animation');
  if (window.history.pushState) {
    window.history.pushState(null, null, window.location.href.split('#')[0]);
  }
}

if (window.location.hash) {
  var tabId = window.location.hash.split('#')[1];
  var tab = document.getElementById(tabId);
  var tabContent = document.getElementById(tabId + '-content');

  if (tab) {
    setTimeout(function() {
      document.getElementById(tabId).click();
    }, 0);
  }
}

function closeMainMenu() {
  var navigationLinks = document.querySelectorAll('.p-navigation__dropdown-link:not(.is-selected)');

  navigationLinks.forEach(function(navLink) {
    navLink.classList.remove('is-open');
  });

  if (!dropdownWindowOverlay.classList.contains('fade-animation')) {
    dropdownWindowOverlay.classList.add('fade-animation');
  }

  if (!dropdownWindow.classList.contains('slide-animation')) {
    dropdownWindow.classList.add('slide-animation');
  }
}

var origin = window.location.href;

addGANavEvents('#products-nav', 'canonical.com-nav-products');
addGANavEvents('#partners-nav', 'canonical.com-nav-partners');
addGANavEvents('#careers-nav', 'canonical.com-nav-careers');

function addGANavEvents(target, category){
  var t = document.querySelector(target);
  if (t) {
    t.querySelectorAll('a').forEach(function(a) {
      a.addEventListener('click', function(){
        dataLayer.push({
          'event' : 'GAEvent',
          'eventCategory' : category,
          'eventAction' : `from:${origin} to:${a.href}`,
          'eventLabel' : a.text,
          'eventValue' : undefined
        });
      });
    });
  }
}

addGAContentEvents('#main-content')

function addGAContentEvents(target){
  var t = document.querySelector(target);
  if (t) {
    t.querySelectorAll('a').forEach(function(a) {
      if (a.className.includes('p-button--positive')) {
        var category = 'www.ubuntu.com-content-cta-0';
      } else if (a.className.includes('p-button')) {
        var category = 'www.ubuntu.com-content-cta-1';
      } else {
        var category = 'www.ubuntu.com-content-link';
      }
      if (!a.href.startsWith("#")){
        a.addEventListener('click', function(){
          dataLayer.push({
            'event' : 'GAEvent',
            'eventCategory' : category,
            'eventAction' : `from:${origin} to:${a.href}`,
            'eventLabel' : a.text,
            'eventValue' : undefined
          });
        });
      }
    });
  }
}

addGAImpressionEvents('.js-takeover')

function addGAImpressionEvents(target){
  var t = document.querySelectorAll(target);
  if (t) {
    t.forEach(function(section) {
      if (! section.className.includes('u-hide')){
        var a = section.querySelector("a");
        dataLayer.push({
          'event' : 'NonInteractiveGAEvent',
          'eventCategory' : "www.ubuntu.com-impression",
          'eventAction' : `from:${origin} to:${a.href}`,
          'eventLabel' : a.text,
          'eventValue' : undefined,
        });
      }
    });
  }
}

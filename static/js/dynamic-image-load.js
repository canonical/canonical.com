(function () {
  var partners = document.querySelectorAll('.js-partner-logos');
  var partnerLinks = document.querySelectorAll('.js-partner-link');

  partnerLinks.forEach(function(partnerLink) {
    partnerLink.addEventListener('mouseover', function(e) {
      loadImages(e.target);
    });
  });
  
  function debounce(func, wait, immediate) {
    var timeout;
    return function () {
      var context = this,
        args = arguments;
      clearTimeout(timeout);
      timeout = setTimeout(function () {
        timeout = null;
        if (!immediate) func.apply(context, args);
      }, wait);
      if (immediate && !timeout) func.apply(context, args);
    };
  }

  var loadImages = debounce(function (el) {
    partners.forEach(function (partner) {
      if ((partner.classList.value.split(" ")[2] === "loaded") && (el.innerHTML.toLowerCase().replace(" ","-"))) {
        Array.from(partner.children).forEach(function (image) {
          image.firstElementChild.dataset.src = image.firstElementChild.src;
          image.firstElementChild.removeAttribute("src");
        });
        partner.classList.remove('loaded');
      }
      if (partner.dataset.partner === el.innerHTML.toLowerCase().replace(" ","-")) {
        Array.from(partner.children).forEach(function (image) {
          image.firstElementChild.src = image.firstElementChild.dataset.src;
          image.firstElementChild.removeAttribute("data-src");
        });
        partner.classList.add('loaded');
      }
    })
  }, 500);
})();
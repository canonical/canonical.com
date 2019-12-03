function highlightInViewNav() {
  var targetElements = document.querySelectorAll('.js-active-target');

  if (targetElements) {
    window.addEventListener('scroll', function() {
      for (i = 0; i < targetElements.length; i++) {
        var el = targetElements[i];
        var scrollPadding = 200;
        var elTop = (el.offsetTop - window.innerHeight) + scrollPadding;
        var elBottom = elTop + el.offsetHeight;
        var cta = document.getElementById('cta--' + el.getAttribute('id'));

        if (window.scrollY > elTop && window.scrollY < elBottom) {
          cta.classList.add('active');
        } else {
          cta.classList.remove('active');
        }
      }
    });
  }
}

highlightInViewNav();
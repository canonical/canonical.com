function setUpTogglableSideNav() {
  var navigationDrawer = document.querySelector("#drawer");
  var navigationDrawerToggles = Array.prototype.slice.call(
    document.querySelectorAll(".js-drawer-toggle"
  ));

  var navigationLinks = Array.prototype.slice.call(
    navigationDrawer.querySelectorAll("a")
  );

  navigationDrawerToggles.forEach(function(toggle) {
    toggle.addEventListener("click", function() {
      navigationDrawer.classList.toggle("is-expanded");
    });
  });

  navigationLinks.forEach(function(link) {
    link.addEventListener("click", function() {
      navigationDrawer.classList.remove("is-expanded");
    });
  });
};

function setUpDynamicSideNav() {
  const questions = Array.prototype.slice.call(
    document.querySelectorAll(".question-heading")
  );

  const navigationLinks = Array.prototype.slice.call(
    document.querySelectorAll(".highlight-link")
  );

  questions.forEach(function(question) {
    const observer = new IntersectionObserver(function(entry) {
      if (entry[0].isIntersecting) {
        const questionId = entry[0].target.id;
        navigationLinks.forEach(function(link) {
          if (link.getAttribute("href") === `#${questionId}`) {
            link.classList.add("is-active");
          } else {
            link.classList.remove("is-active");
          }
        });
      }
    }, {
      rootMargin: "-200px 0px -400px",
      threshold: 0.5,
    });

    observer.observe(question);
  });
};

(function() {
  setUpTogglableSideNav();
  setUpDynamicSideNav();
})();

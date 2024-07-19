// Sliding js from vanilla, also handle dropdowns?
const initNavigationSliding = () => {
  const secondaryNavigation = document.querySelector(
    ".p-navigation--reduced + .p-navigation"
  );
  const searchButtons = document.querySelectorAll(".js-search-button");
  // const menuButton = document.querySelector(".js-menu-button");
  const dropdowns = document.querySelectorAll("ul.p-navigation__dropdown");
  const lists = [...dropdowns];
  const mainList = dropdowns[0]?.parentNode?.parentNode;
  if (mainList) {
    lists.push(mainList);
  }

  const hasSearch = searchButtons.length > 0;

  // const closeAllNavigationItems = () => {
  //   console.log("closeAllNavigationItems");
  //   resetMainToggles();
  //   navigation.classList.remove("has-menu-open");
  //   if (secondaryNavigation) {
  //     secondaryNavigation.classList.remove("has-menu-open");
  //   }
  //   menuButton.innerHTML = "Menu";
  // };

  // const resetMainToggles = (exception) => {
  //   console.log("Reseting toggle");
  //   mainToggles.forEach(function (toggle) {
  //     const target = document.getElementById(
  //       toggle.getAttribute("aria-controls")
  //     );
  //     if (!target || target === exception) {
  //       return;
  //     }
  //     target.setAttribute("aria-hidden", "true");
  //     toggle.parentNode.classList.remove("is-active");
  //     toggle.parentNode.parentNode.classList.remove("is-active");
  //   });
  // };

  const setFocusable = (target) => {
    lists.forEach(function (list) {
      const elements = list.querySelectorAll("ul > li > a, ul > li > button");
      elements.forEach(function (element) {
        element.setAttribute("tabindex", "-1");
      });
    });
    if (target) {
      target.querySelectorAll("li").forEach(function (element) {
        if (element.parentNode === target) {
          element.children[0].setAttribute("tabindex", "0");
        }
      });
    }
  };

  const goBackOneLevel = (e, backButton) => {
    e.preventDefault();
    const target = backButton.closest(".p-navigation__dropdown");
    target.setAttribute("aria-hidden", "true");
    backButton.closest(".is-active").classList.remove("is-active");
    backButton.closest(".is-active").classList.remove("is-active");
    setFocusable(target.parentNode.parentNode);
  };

  dropdowns.forEach(function (dropdown) {
    dropdown.children[1].addEventListener("keydown", function (e) {
      if (
        e.shiftKey &&
        e.key === "Tab" &&
        window.getComputedStyle(dropdown.children[0], null).display === "none"
      ) {
        goBackOneLevel(e, dropdown.children[1].children[0]);
        dropdown.parentNode.children[0].focus({ preventScroll: true });
      }
    });
  });

  document.querySelectorAll(".js-back").forEach(function (backButton) {
    backButton.addEventListener("click", function (e) {
      goBackOneLevel(e, backButton);
    });
  });
};

initNavigationSliding();

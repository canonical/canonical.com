(function () {
  const setActiveTab = (tab, tabs) => {
    tabs.forEach((tabElement) => {
      if (tabElement === tab) {
        tabElement.setAttribute("aria-current", "page");
      } else {
        tabElement.removeAttribute("aria-current");
      }
    });
    updateCards(tab.getAttribute("aria-controls"));
  };

  const updateCards = (targetCategory) => {
    const productCardsContainer = document.getElementById("product-container");
    const productCards = [].slice.call(productCardsContainer.querySelectorAll("[data-categories]"));
    productCards.forEach((productCard) => {
      if (productCard.getAttribute("data-categories").includes(targetCategory)) {
        productCard.style.display = "block";
      } else {
        productCard.style.display = "none";
      }
    });
  };

  const attachEvents = (tabs) => {
    tabs.forEach((tab) => {
      tab.addEventListener("click", (e) => {
        e.preventDefault();
        setActiveTab(tab, tabs);
      });
    });
  };

  const init = (selector) => {
    const tabContainers = [].slice.call(document.querySelectorAll(selector));
    tabContainers.forEach((tabContainer) => {
      var tabs = [].slice.call(tabContainer.querySelectorAll("[aria-controls]"));
      attachEvents(tabs);
    });
  };

  document.addEventListener("DOMContentLoaded", () => {
    init('[role="tablist"]');
  });
})();

(function () {
  const setActiveTab = (tab, tabs) => {
    tabs.forEach((tabElement) => {
      if (tabElement === tab) {
        tabElement.setAttribute("aria-current", "page");
      } else {
        tabElement.removeAttribute("aria-current");
      }
    });
  };

  const attachEvents = (tabs) => {
    tabs.forEach((tab) => {
      tab.addEventListener("click", (e) => {
        setActiveTab(tab, tabs);
      });
    });
  };

  const init = (selector) => {
    const tabContainer = document.querySelector(selector);
    const tabs = [].slice.call(tabContainer.querySelectorAll("[aria-controls]"));
    attachEvents(tabs);
  };

  document.addEventListener("DOMContentLoaded", () => {
    init('[role="tablist"]');
  });
})();

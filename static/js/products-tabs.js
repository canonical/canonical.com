(function () {
  const setActiveTab = (tab, tabs) => {
    tabs.forEach((tabElement) => {
      const tabContent = document.getElementById(tabElement.getAttribute("aria-controls"));
      if (tabElement === tab) {
        tabElement.setAttribute("aria-current", "page");
        tabContent.removeAttribute("hidden");
      } else {
        tabElement.removeAttribute("aria-current");
        tabContent.setAttribute("hidden", "true");
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
    const tabContainer = document.querySelector(selector);
    const tabs = [].slice.call(tabContainer.querySelectorAll("[aria-controls]"));
    attachEvents(tabs);

    setActiveTab(tabs[0], tabs);
  };

  document.addEventListener("DOMContentLoaded", () => {
    init('[role="tablist"]');
  });
})();

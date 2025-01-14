(function () {
  const tabListContainers = document.querySelectorAll("[role='tablist']");
  const buttonContainers = document.querySelectorAll(".js-tab-buttons");

  const keys = {
    left: "ArrowLeft",
    right: "ArrowRight",
  };

  const direction = {
    ArrowLeft: -1,
    ArrowRight: 1,
  };

  // IE11 doesn't support event.code, but event.keyCode is
  // deprecated in most modern browsers, so we should support
  // both for the time being.
  const IEKeys = {
    left: 37,
    right: 39,
  };

  const IEDirection = {
    37: direction["ArrowLeft"],
    39: direction["ArrowRight"],
  };

  /**
      Determine which tab to show when an arrow key is pressed
      @param {KeyboardEvent} event
      @param {Array} tabs an array of tabs within a container
    */
  const switchTabOnArrowPress = (event, tabs) => {
    let compatibleKeys = IEKeys;
    let compatibleDirection = IEDirection;
    let pressed = event.keyCode;

    if (event.code) {
      compatibleKeys = keys;
      compatibleDirection = direction;
      pressed = event.code;
    }

    if (compatibleDirection[pressed]) {
      const target = event.target;
      if (target.index !== undefined) {
        if (tabs[target.index + compatibleDirection[pressed]]) {
          tabs[target.index + compatibleDirection[pressed]].focus();
        } else if (pressed === compatibleKeys.left) {
          tabs[tabs.length - 1].focus();
        } else if (pressed === compatibleKeys.right) {
          tabs[0].focus();
        }
      }
    }
  };

  /**
      Attaches a number of events that each trigger
      the reveal of the chosen tab content
      @param {Array} tabs an array of tabs within a container
    */
  const attachEvents = (
    tabs,
    persistURLHash,
    prevButton,
    nextButton,
    tabContainer
  ) => {
    tabs.forEach(function (tab, index) {
      tab.addEventListener("keyup", function (e) {
        let compatibleKeys = IEKeys;
        let key = e.keyCode;

        if (e.code) {
          compatibleKeys = keys;
          key = e.code;
        }

        if (key === compatibleKeys.left || key === compatibleKeys.right) {
          switchTabOnArrowPress(e, tabs);
        }
      });

      tab.addEventListener("click", (e) => {
        e.preventDefault();

        if (persistURLHash) {
          // if we're adding the ID of the tab to the URL
          // this prevents the page attempting to jump to
          // the section with that ID
          history.pushState({}, "", tab.href);

          // Update the URL again with the same hash, then go back
          history.pushState({}, "", tab.href);
          history.back();
        }

        setActiveTab(tab, tabs);

        // Add focus to the tab panel on tab click
        const tabPanel = document.getElementById(tab.id + "-tab");

        if (tabPanel) {
          tabPanel.focus({ preventScroll: true });
        }

        // For tablist containers with pagination
        // toggle buttons state on tab click
        if (prevButton && nextButton) {
          if (index === 0) {
            prevButton.disabled = true;
            nextButton.disabled = false;
          } else if (index > 0 && index < tabs.length - 1) {
            prevButton.disabled = false;
            nextButton.disabled = false;
          } else {
            prevButton.disabled = false;
            nextButton.disabled = true;
          }
        }
      });

      tab.addEventListener("focus", () => {
        setActiveTab(tab, tabs);
      });

      tab.index = index;
    });

    // For tab list containers with pagination buttons
    // set the active tab on button click
    if (prevButton && nextButton) {
      prevButton.addEventListener("click", (e) => {
        e.preventDefault();
        const currentTab = tabContainer.querySelector(
          ".p-tabs__item[aria-selected='true']"
        );
        const currentIndex = tabs.indexOf(currentTab);
        const prevIndex =
          currentIndex === 0 ? tabs.length - 1 : currentIndex - 1;

        nextButton.disabled = false;

        if (currentIndex === 1) {
          prevButton.disabled = true;
        }

        setActiveTab(tabs[prevIndex], tabs);
      });

      nextButton.addEventListener("click", (e) => {
        e.preventDefault();
        const currentTab = tabContainer.querySelector(
          ".p-tabs__item[aria-selected='true']"
        );
        const currentIndex = tabs.indexOf(currentTab);
        const nextIndex =
          currentIndex === tabs.length - 1 ? 0 : currentIndex + 1;

        prevButton.disabled = false;

        if (currentIndex === tabs.length - 2) {
          nextButton.disabled = true;
        }

        setActiveTab(tabs[nextIndex], tabs);
      });
    }
  };

  /**
      Cycles through an array of tab elements and ensures
      only the target tab and its content are selected
      @param {HTMLElement} tab the tab whose content will be shown
      @param {Array} tabs an array of tabs within a container
    */
  const setActiveTab = (tab, tabs) => {
    tabs.forEach((tabElement) => {
      var tabContent = document.querySelectorAll(
        "#" + tabElement.getAttribute("aria-controls")
      );
      tabContent.forEach((content) => {
        if (tabElement === tab) {
          tabElement.setAttribute("aria-selected", true);
          content.classList.remove("u-hide");
        } else {
          tabElement.setAttribute("aria-selected", false);
          content.classList.add("u-hide");
        }
      });
    });
  };

  /**
    Attaches events to tab links within a given parent element,
    and sets the active tab if the current hash matches the id
    of an element controlled by a tab link
    @param {String} selector class name of the element
    containing the tabs we want to attach events to
  */
  const initTabs = (selector) => {
    var tabContainers = [].slice.call(document.querySelectorAll(selector));

    tabContainers.forEach((tabContainer) => {
      // if the tab container has this data attribute, the id of the tab
      // is added to the URL, and a particular tab can be directly linked
      var persistURLHash = tabContainer.getAttribute("data-maintain-hash");
      var currentHash = window.location.hash;
      let prevButton, nextButton;

      var tabs = [].slice.call(
        tabContainer.querySelectorAll("[aria-controls]")
      );

      // If the tab list container has pagination buttons
      // define the target buttons by matching the tablist data attribute
      // to the button container ID
      if (buttonContainers) {
        buttonContainers.forEach((buttonContainer) => {
          if (buttonContainer.id === tabContainer.dataset.tablist) {
            prevButton = buttonContainer.querySelector(".js-prev-tab");
            nextButton = buttonContainer.querySelector(".js-next-tab");
          }
        });
      }

      attachEvents(tabs, persistURLHash, prevButton, nextButton, tabContainer);

      if (persistURLHash && currentHash) {
        var activeTab = document.querySelector(
          ".p-tabs__link[href='" + currentHash + "']"
        );

        if (activeTab) {
          setActiveTab(activeTab, tabs);
        }
      } else {
        setActiveTab(tabs[0], tabs);
      }
    });
  };

  (function () {
    // Toggles show board based on selection on small screens

    const boards = document.querySelectorAll(`[role=tabpanel]`);
    const dropdownSelect = document.getElementById("boardSelect");

    dropdownSelect?.addEventListener("change", (event) => {
      selectBoard();
    });

    function selectBoard() {
      boards.forEach((board) => {
        if (board.id === dropdownSelect.value) {
          board.classList.remove("u-hide");
          board.focus();
        } else {
          board.classList.add("u-hide");
        }
      });
    }
  })();

  document.addEventListener("DOMContentLoaded", () => {
    initTabs(".js-tabbed-content");
  });
})();

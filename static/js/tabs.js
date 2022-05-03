(function () {
  var keys = {
    left: "ArrowLeft",
    right: "ArrowRight",
  };

  var direction = {
    ArrowLeft: -1,
    ArrowRight: 1,
  };

  function initTabs(selector) {
    var tabContainers = [].slice.call(document.querySelectorAll(selector));

    tabContainers.forEach(function (tabContainer) {
      var tabs = [].slice.call(tabContainer.querySelectorAll("[aria-controls]"));
      preventPageJump(tabs);
      attachEvents(tabs);
    });
  }

  function preventPageJump(tabs) {
    // prevent the page jumping around when switching tabs,
    // whilst still using :target
    // https://gist.github.com/pimterry/260841c2104f27cadc954a29b9873b96#file-disable-link-jump-with-workaround-js
    [].forEach.call(tabs, function (link) {
      link.addEventListener("click", function (event) {
        event.preventDefault();
        history.pushState({}, "", link.href);

        // Update the URL again with the same hash, then go back
        history.pushState({}, "", link.href);
        history.back();
      });
    });
  }

  function attachEvents(tabs) {
    tabs.forEach(function (tab, index) {
      tab.addEventListener("keyup", function (e) {
        if (e.code === keys.left || e.code === keys.right) {
          switchTabOnArrowPress(e, tabs);
        }
      });

      tab.addEventListener("click", function (e) {
        e.preventDefault();
        setActiveTab(tab, tabs);
      });

      tab.addEventListener("focus", function () {
        setActiveTab(tab, tabs);
      });

      tab.index = index;
    });
  }

  function switchTabOnArrowPress(event, tabs) {
    var pressed = event.code;

    if (direction[pressed]) {
      var target = event.target;
      if (target.index !== undefined) {
        if (tabs[target.index + direction[pressed]]) {
          tabs[target.index + direction[pressed]].focus();
        } else if (pressed === keys.left) {
          tabs[tabs.length - 1].focus();
        } else if (pressed === keys.right) {
          tabs[0].focus();
        }
      }
    }
  }

  function setActiveTab(tab, tabs) {
    console.log(tabs);
    tabs.forEach(function (tabElement) {
      var tabContent = document.getElementById(tabElement.getAttribute("aria-controls"));
      console.log(tabElement);
      if (tabElement === tab) {
        console.log("Removing hidden from", tabContent);
        tabElement.setAttribute("aria-selected", true);
        tabContent.removeAttribute("hidden");
      } else {
        console.log("its not a match");
        tabElement.setAttribute("aria-selected", false);
        tabContent.setAttribute("hidden", true);
      }
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initTabs('[role="tablist"]');
  });
})();

(function () {
  /** @type {HTMLInputElement} */
  const searchBox = document.querySelector(".js-find-a-partner__search-input");
  const urlParams = new URLSearchParams(window.location.search);
  const partners = document.querySelectorAll(".js-find-a-partner__partner");
  /** @type {NodeListOf<HTMLInputElement>} */
  const checkboxes = document.querySelectorAll(".js-find-a-partner__filter");
  const searchResetButton = document.querySelector(".p-search-box__reset");
  const noResults = document.querySelector(".js-find-a-partner__no-results");
  const sideNavButtons = document.querySelectorAll(".js-accordion-toggle");
  const clearFiltersButton = document.getElementById("js-clear-filters");

  var filters = [];

  function init() {
    revealSearch();
    retainCheckedFilters();

    if (searchBox) {
      populateTextbox();
      searchDom();
      searchBox.addEventListener("keyup", searchHandler);
    }

    populateCheckboxes();

    updateFilterList();

    if (checkboxes) {
      filterDom();
      checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener("change", filterHandler);
      });
    }

    if (searchResetButton) {
      searchResetButton.addEventListener("click", searchHandler);
    }

    updateNumberOfPartners();

    if (sideNavButtons) {
      sideNavButtons.forEach((el) => {
        el.addEventListener("click", function () {
          toggleSection(el);
        });
      });
    }

    if (clearFiltersButton) {
      clearFiltersButton.addEventListener("click", clearFilters);
    }
  }

  // Toggle side nav accordions
  function toggleSection(el) {
    if (el) {
      let targetPanel = el.parentElement.parentElement.querySelector(
        ".p-accordion__panel"
      );

      el.ariaExpanded = el.ariaExpanded !== "true";
      targetPanel.ariaHidden = targetPanel.ariaHidden !== "true";
    }
  }

  // Display no reults message
  function updateNoResultsMessage() {
    let filteredCount = document.querySelectorAll(
      ".js-find-a-partner__partner.js-searched.js-filtered"
    ).length;

    if (noResults) {
      if (filteredCount === 0) {
        noResults.classList.remove("u-hide");
      } else {
        noResults.classList.add("u-hide");
      }
    }
  }

  // Show search and filter functionality if JS is available
  function revealSearch() {
    var searchForm = document.querySelector(".js-search-form");
    if (searchForm) {
      searchForm.classList.remove("u-hide");
    }
  }

  // Debounced search handler function
  searchHandler = debounce(function (e) {
    searchDom();
    updateNumberOfPartners();
    updateNoResultsMessage();
    updateUrl("search", searchBox.value);
  }, 350);

  function searchDom() {
    if (partners) {
      partners.forEach(function (partner) {
        partner.classList.remove("js-searched");
        var searchText = partner.getAttribute("data-searchText").toLowerCase();

        if (searchText.includes(searchBox.value.toLowerCase())) {
          partner.classList.add("js-searched");
        }
      });
    }
  }

  function filterHandler() {
    updateFilterList();
    filterDom();
    updateNumberOfPartners();
    updateNoResultsMessage();
    updateUrl("filters", filters);
    toggleClearButton();
  }

  function filterDom() {
    if (filters.length === 0 && partners) {
      partners.forEach((partner) => {
        partner.classList.add("js-filtered");
      });
    } else if (partners) {
      partners.forEach((partner) => {
        partner.classList.remove("js-filtered");
        var filterText = partner.getAttribute("data-filter").toLowerCase();
        if (filterCheck(filterText)) {
          partner.classList.add("js-filtered");
        }
      });
    }
  }

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

  // Hide clear filters button if there are no selected filters
  function toggleClearButton() {
    if (filters.length > 0) {
      clearFiltersButton.classList.remove("u-hide");
    } else {
      clearFiltersButton.classList.add("u-hide");
    }
  }

  // Update browser url updateUrl
  function updateUrl(type, value) {
    const currentUrl = window.location.href;
    const baseUrl = currentUrl.split("?")[0];
    var newUrl = baseUrl;

    if (!(searchBox.value === "") && filters.length > 0) {
      filtersString = "";
      filters.forEach((filter, i) => {
        if (i === filters.length - 1) {
          filtersString += filter;
        } else {
          filtersString += `${filter},`;
        }
      });
      newUrl = `${baseUrl}?search=${searchBox.value}&filters=${filtersString}`;
    }
    if (!(searchBox.value === "") && filters.length === 0) {
      newUrl = `${baseUrl}?search=${searchBox.value}`;
    }
    if (searchBox.value === "" && filters.length > 0) {
      filtersString = "";
      filters.forEach((filter, i) => {
        if (i === filters.length - 1) {
          filtersString += filter;
        } else {
          filtersString += `${filter},`;
        }
      });
      newUrl = `${baseUrl}?filters=${filtersString}`;
    }
    window.history.pushState(
      { search: searchBox.value, filters: filters },
      "",
      newUrl
    );
  }

  // Retain checked filters on page load
  function retainCheckedFilters() {
    if (urlParams.has("filters")) {
      let loadedFilters = urlParams.get("filters").split(",");

      loadedFilters.forEach((filter) => {
        checkboxes.forEach((box) => {
          if (box.name === filter) {
            box.checked = true;
          }
        });
      });
    }
  }

  // Check if element should be filtered
  function filterCheck(filterText) {
    var match = false;
    filters.forEach((filter) => {
      if (filterText.includes(filter) && !match) {
        match = true;
      }
    });
    return match;
  }

  // Update filters array to match checked checkboxes
  function updateFilterList() {
    if (checkboxes) {
      filters = [];
      checkboxes.forEach((checkbox) => {
        if (checkbox.checked) {
          if (filters.includes(checkbox.name)) {
            let index = filters.indexOf(checkbox.name);
            filters.splice(index, 1);
          } else {
            filters.push(checkbox.name);
          }
        }
      });
    }
  }

  // Clear all applied filters
  function clearFilters() {
    if (checkboxes) {
      checkboxes.forEach((box) => {
        box.checked = false;
      });
    }
    filterHandler();
  }

  // Check any checkboxes that match URL filters query
  function populateCheckboxes() {
    const queryFilters = urlParams.get("filters");
    if (queryFilters) {
      queryFilters.split(",").forEach((filter) => {
        var checkboxObject = document.querySelector("#" + filter);
        if (checkboxObject) {
          checkboxObject.checked = true;
        }
      });
    }
  }

  // Update search box text with data from query params
  function populateTextbox() {
    const querySearchText = urlParams.get("search");
    if (searchBox && querySearchText) {
      searchBox.focus();
      searchBox.value = querySearchText;
    }
  }

  // Update number of partners mtachig search and/or filter criteria
  function updateNumberOfPartners() {
    const partnersCountElement = document.getElementById("partners-count");

    let filteredCount = document.querySelectorAll(
      ".js-find-a-partner__partner.js-searched.js-filtered"
    ).length;

    if (filteredCount == partnersLength) {
      partnersCountElement.innerHTML = "All " + filteredCount + " partners";
    } else if (filteredCount === 1) {
      partnersCountElement.innerHTML = filteredCount + " partner";
    } else {
      partnersCountElement.innerHTML = filteredCount + " partners";
    }

    updateNoResultsMessage();
  }

  init();
})();

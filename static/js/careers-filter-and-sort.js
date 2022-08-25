(function () {
  const urlParams = new URLSearchParams(window.location.search);
  const domList = document.querySelector(".js-job-list");
  const show20MoreEl = document.getElementById("show-20-more");
  const filterSelect = document.querySelector(".js-filter");
  const noResults = document.querySelector(".js-filter__no-results");
  const jobContainer = document.querySelector(".js-filter-jobs-container");
  const sortSelect = document.querySelector(".js-sort");
  const locationSelect = document.querySelector(".js-filter--location");
  const searchBox = document.querySelector(".js-careers__search-input");
  // Show search and filter functionality if JS is available
  function revealSearch() {
    const searchForm = document.querySelector(".js-search-jobs-form");
    if (searchForm) {
      searchForm.classList.remove("u-hide");
    }
  }
  var numberOfJobsDisplayed = 0;
  var filterBy = {};

  // Read data-location property and parse locations into well-defined categories
  function parseLocations() {
    const regions = {
      europe: [
        "emea",
        "slovakia",
        "bratislava",
        "europe",
        "uk",
        "germany",
        "berlin",
        "london",
        "worldwide",
      ],
      americas: [
        "americas",
        "southwest",
        "san francisco",
        "usa",
        "austin",
        "texas",
        "tx",
        "brazil",
        "seattle",
        "america",
        "worldwide",
      ],
      asia: ["apac", "taiwan", "taipei", "beijing", "china", "worldwide"],
      "middle-east": ["emea", "worldwide"],
      africa: ["emea", "worldwide"],
      oceania: ["apac", "worldwide"],
    };

    const jobsList = document.querySelector(".js-job-list")?.children || [];
    for (let n = 0; n < jobsList.length; n++) {
      const location = jobsList[n].getAttribute("data-location");
      var locationsList = "";

      for (let region in regions) {
        const regionalLocations = regions[region];

        for (let i = 0; i < regionalLocations.length; i++) {
          if (location.toLowerCase().includes(regionalLocations[i])) {
            locationsList += region + " ";
            break;
          }
        }
      }

      if (locationsList.length > 0) {
        locationsList = locationsList.slice(0, locationsList.length - 1);
      }
      jobsList[n].setAttribute("location-filter", locationsList);
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

  function slice(elements, start, end) {
    const sliced = Array.prototype.slice.call(elements, start, end);
    return sliced;
  }

  function init() {
    revealSearch();
    revealFilters();
    if (searchBox) {
      populateTextbox();
    }
    if (domList.length === 0) {
      updateNoResultsMessage();
    }
    if (domList) {
      parseLocations();

      // Save original list
      if (!window.careersJobList) {
        window.careersJobList = domList.cloneNode(true);
      }
      
      show20MoreEl.addEventListener("click", (e) => {
        e.preventDefault();
        console.log("after click", window.careersJobList.childElementCount)
        if (domList.childElementCount < window.careersJobList.childElementCount) {
          let currentListRolesNodesCount = domList.childElementCount - 1;
          const offsetListRolesNodesCount = currentListRolesNodesCount + 20;
          const previousCareersJobList = window.careersJobList.cloneNode(true)
          const listChildrenRolesNodes = slice(window.careersJobList.children, currentListRolesNodesCount, offsetListRolesNodesCount);
          window.careersJobList = previousCareersJobList
          domList.append(...listChildrenRolesNodes)
        } else {
          show20MoreEl.classList.add("u-hidden")
        }
        
      })

      if (window.careersJobList.childElementCount > 20) {
        const listChildrenRolesNodes = slice(domList.children, 0, 20);
        domList.replaceChildren(...listChildrenRolesNodes)
      }



      var jobList = Array.from(domList.children);
      if (filterSelect && filterSelect.options) {
        // Get list of options from the HTML form
        var filterOptions = [];
        Array.from(filterSelect.options).forEach(function (el) {
          filterOptions.push(el.value);
        });
      

        if (urlParams.has("filter")) {
          // If the page is loaded with inital URL parameters, change the default form selection and filter the results to reflect this
          var filterValue = urlParams.get("filter");
          for (let n = 0; n < filterOptions.length; n++) {
            if (filterOptions[n] === filterValue) {
              filterSelect.options.selectedIndex = n;
              break;
            }
          }
        }

        updateFilterBy(
          filterSelect.options[filterSelect.options.selectedIndex].value
        );

        // Add event listener that will update the URL and filter the results if the selected option is changed
        filterSelect.addEventListener("change", function () {
          if (!(sortSelect.options.selectedIndex === 0)) {
            sortSelect.options.selectedIndex = 0;
          }
          updateFilterBy(
            filterSelect.options[filterSelect.options.selectedIndex].value
          );
          filterJobs(filterBy, jobList);
          updateURL(filterBy);
          updateNoResultsMessage();
        });
      }

      if (locationSelect) {
        // Get list of options from the HTML form
        var locationOptions = [];
        Array.from(locationSelect.options).forEach(function (el) {
          locationOptions.push(el.value);
        });

        if (urlParams.has("location")) {
          // If the page is loaded with inital URL parameters, change the default form selection and filter the results to reflect this
          var locationValue = urlParams.get("location");
          for (var n = 0; n < locationOptions.length; n++) {
            if (locationOptions[n] === locationValue) {
              locationSelect.options.selectedIndex = n;
              break;
            }
          }
        }

        updateLocationFilterBy(
          locationSelect.options[locationSelect.options.selectedIndex].value
        );

        // Add event listener that will update the URL and filter the results if the selected option is changed
        locationSelect.addEventListener("change", function () {
          if (!(sortSelect.options.selectedIndex === 0)) {
            sortSelect.options.selectedIndex = 0;
          }
          updateLocationFilterBy(
            locationSelect.options[locationSelect.options.selectedIndex].value
          );
          filterJobs(filterBy, jobList);
          updateURL(filterBy);
          updateNoResultsMessage();
        });
      }

      filterJobs(filterBy, jobList);
      updateNoResultsMessage();

      if (sortSelect) {
        sortSelect.addEventListener("change", function (e) {
          jobList.sort((a, b) =>
            a.dataset[sortSelect.value] !== b.dataset[sortSelect.value]
              ? a.dataset[sortSelect.value] < b.dataset[sortSelect.value]
                ? -1
                : 1
              : 0
          );
          if (sortSelect.value === "date") {
            jobList.reverse();
          }
          // Create new DOM list
          const sortedDomList = document.createDocumentFragment();
          jobList.forEach((el) => {
            sortedDomList.appendChild(el);
          });
          // Empty the DOM
          while (domList.children.length > 1) {
            domList.removeChild(domList.firstChild);
          }
          domList.appendChild(sortedDomList);
        });
      }
    }
  }

  // Show filters if JS is available
  function revealFilters() {
    var filterForm = document.querySelector(".js-filter-form");
    if (filterForm) {
      filterForm.classList.remove("u-hide");
    }
  }

  function filterJobs(filterBy, jobList) {
    numberOfJobsDisplayed = domList.childElementCount;
    jobList.forEach(function (node) {

      if (filterBy.filterText === "All" && filterBy.location === "all") {
        if (node.classList.contains("u-hide")) {
          node.classList.remove("u-hide");
        }
        numberOfJobsDisplayed = domList.childElementCount;
      } else if (
        filterBy.filterValue !== "all" &&
        filterBy.location === "all"
      ) {
        if (node.dataset[filterBy.filterName].includes(filterBy.filterText)) {
          if (node.classList.contains("u-hide")) {
            node.classList.remove("u-hide");
          }
        } else {
          if (!node.classList.contains("u-hide")) {
            node.classList.add("u-hide");
          }
          numberOfJobsDisplayed--;
        }
      } else if (
        filterBy.filterValue === "all" &&
        filterBy.location !== "all"
      ) {
        if (node.getAttribute("location-filter").includes(filterBy.location)) {
          if (node.classList.contains("u-hide")) {
            node.classList.remove("u-hide");
          }
        } else {
          if (!node.classList.contains("u-hide")) {
            node.classList.add("u-hide");
          }
          numberOfJobsDisplayed--;
        }
      } else {
        if (
          node.dataset[filterBy.filterName].includes(filterBy.filterText) &&
          node.getAttribute("location-filter").includes(filterBy.location)
        ) {
          if (node.classList.contains("u-hide")) {
            node.classList.remove("u-hide");
          }
        } else {
          if (!node.classList.contains("u-hide")) {
            node.classList.add("u-hide");
          }
          numberOfJobsDisplayed--;
        }
      }
    });
  }

  function updateFilterBy(filter) {
    switch (filter) {
      case "home-based":
        filterBy.filterName = "office";
        filterBy.filterText = "Home Based";
        filterBy.filterValue = "home-based";
        break;
      case "office-based":
        filterBy.filterName = "office";
        filterBy.filterText = "Office Based";
        filterBy.filterValue = "office-based";
        break;
      case "management":
        filterBy.filterName = "management";
        filterBy.filterText = "True";
        filterBy.filterValue = "management";
        break;
      case "full-time":
        filterBy.filterName = "employment";
        filterBy.filterText = "Full-time";
        filterBy.filterValue = "full-time";
        break;
      case "part-time":
        filterBy.filterName = "employment";
        filterBy.filterText = "Part-time";
        filterBy.filterValue = "part-time";
        break;
      default:
        filterBy.filterName = "all";
        filterBy.filterText = "All";
        filterBy.filterValue = "all";
    }
  }

  function updateLocationFilterBy(location) {
    switch (location) {
      case "europe":
        filterBy.location = "europe";
        break;
      case "americas":
        filterBy.location = "americas";
        break;
      case "asia":
        filterBy.location = "asia";
        break;
      case "middle-east":
        filterBy.location = "middle-east";
        break;
      case "africa":
        filterBy.location = "africa";
        break;
      case "oceania":
        filterBy.location = "oceania";
        break;
      default:
        filterBy.location = "all";
    }
  }

  // Display no reults message
  function updateNoResultsMessage() {
    if (noResults && jobContainer) {
      if (numberOfJobsDisplayed === 0) {
        noResults.classList.remove("u-hide");
        jobContainer.classList.add("u-hide");
      } else {
        noResults.classList.add("u-hide");
        jobContainer.classList.remove("u-hide");
      }
    }
  }

  function updateURL(filterBy) {
    var baseURL = window.location.origin + window.location.pathname;

    urlParams.set("filter", filterBy.filterValue);
    urlParams.set("location", filterBy.location);

    var url = baseURL + "?" + urlParams.toString() + "#available-roles";

    window.history.pushState({}, "", url);
  }
    window.addEventListener('DOMContentLoaded', (event) => {
      init();
    })
  })();

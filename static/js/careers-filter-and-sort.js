(function () {
  const urlParams = new URLSearchParams(window.location.search);
  const domList = document.querySelector(".js-job-list");
  const filterSelect = document.querySelector(".js-filter");
  const noResults = document.querySelector(".js-filter__no-results");
  const jobContainer = document.querySelector(".js-filter-jobs-container");
  const sortSelect = document.querySelector(".js-sort");

  var numberOfJobsDisplayed = 0;
  var filters = [];
  var filterBy = {};

  function initialiseLocationList()
  {
    const jobsList = document.querySelector(".js-job-list").children;
    var locationList = [];
    for(let n = 0; n<jobsList.length; n++)
    {
      var duplicate = false;
      //var location = jobsList[n].getAttribute("data-location");
      for(let x = 0; x<locationList.length; x++)
      {
        if(locationList[x] === jobsList[n].getAttribute("data-location"))
        {
          duplicate = true;
          break;
        }
      }
      if(!duplicate)
      {
        locationList.push(jobsList[n].getAttribute("data-location"));
      }
    }
    const target = document.querySelector(".js-filter--location");
    for(var n=0; n<locationList.length; n++)
    {
      var fragment = document.createDocumentFragment();
      var option = document.createElement("option");
      //option.setAttribute(value; )
      var text = document.createTextNode(locationList[n]);
      option.appendChild(text);
      target.appendChild(option);
    }
  }

  initialiseLocationList();

  function init() {
    var queryFilter = urlParams.get('filter');

    revealFilters();

    if (domList) {
      var jobList = Array.from(domList.children);

      if (filterSelect) {
        Array.from(filterSelect.options).forEach(function (el) {
          filters.push(el.value);
        });

        if (queryFilter) {
          filterSelect.options.selectedIndex = filters.indexOf(queryFilter);
          updateFilterBy(filterSelect.options[filterSelect.options.selectedIndex].value);
          filterJobs(filterBy, jobList);
          updateNoResultsMessage();
        }

        filterSelect.addEventListener("change", function () {
          if (!(sortSelect.options.selectedIndex === 0)) {
            sortSelect.options.selectedIndex = 0;
          }
          updateFilterBy(filterSelect.options[filterSelect.options.selectedIndex].value);
          filterJobs(filterBy, jobList);
          updateURL(filterBy);
          updateNoResultsMessage();
        });
      }

      if (sortSelect) {
        sortSelect.addEventListener("change", function (e) {
          jobList.sort((a, b) => a.dataset[sortSelect.value] !== b.dataset[sortSelect.value] ? a.dataset[sortSelect.value] < b.dataset[sortSelect.value] ? -1 : 1 : 0);
          if (sortSelect.value === "date") {
            jobList.reverse();
          }
          // Create new DOM list
          const sortedDomList = document.createDocumentFragment();
          jobList.forEach(el => {
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
      if (filterBy.filterText === "All") {
        if (node.classList.contains("u-hide")) {
          node.classList.remove("u-hide");
        }
        numberOfJobsDisplayed = domList.childElementCount;
      } else {
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

    urlParams.set('filter', filterBy.filterValue);

    var url = baseURL + '?' + urlParams.toString() + '#available-roles';

    window.history.pushState({}, "", url);
  }

  init();
})();

(function () {
  const urlParams = new URLSearchParams(window.location.search);
  const domList = document.querySelector(".js-job-list");
  var filterSelect = document.querySelector(".js-filter");
  const noResults = document.querySelector(".js-filter__no-results");
  const jobContainer = document.querySelector(".js-filter-jobs-container");
  const sortSelect = document.querySelector(".js-sort");
  var locationSelect = document.querySelector(".js-filter--location");

  var numberOfJobsDisplayed = 0;
  var filters = [];
  var locationFilters = [];
  var filterBy = {};

  function parseLocations() {
    const europe = ["emea", "slovakia", "bratislava", "europe", "uk", "germany", "berlin", "london", "worldwide"];
    const americas = ["americas", "southwest", "san francisco", "usa", "austin", "texas", "tx", "brazil", "seattle", "america", "worldwide"];
    const asia = ["apac", "taiwan", "taipei", "beijing", "china", "worldwide"];
    const middleEast = ["emea", "worldwide"];
    const africa = ["emea", "worldwide"];
    const oceania = ["apac", "worldwide"];

    const jobsList = document.querySelector(".js-job-list").children;

    for(var n=0; n<jobsList.length; n++)
    {
      const location = jobsList[n].getAttribute("data-location");
      var locationsList = "";

      for(var x=0; x<europe.length; x++)
      {
        if(location.toLowerCase().includes(europe[x]))
        {
          locationsList += "europe ";
          break;
        }
      }
      for(var x=0; x<americas.length; x++)
      {
        if(location.toLowerCase().includes(americas[x]))
        {
          locationsList += "americas ";
          break;
        }
      }
      for(var x=0; x<asia.length; x++)
      {
        if(location.toLowerCase().includes(asia[x]))
        {
          locationsList += "asia ";
          break;
        }
      }
      for(var x=0; x<middleEast.length; x++)
      {
        if(location.toLowerCase().includes(middleEast[x]))
        {
          locationsList += "middle-east ";
          break;
        }
      }
      for(var x=0; x<africa.length; x++)
      {
        if(location.toLowerCase().includes(africa[x]))
        {
          locationsList += "africa ";
          break;
        }
      }
      for(var x=0; x<oceania.length; x++)
      {
        if(location.toLowerCase().includes(oceania[x]))
        {
          locationsList += "oceania ";
          break;
        }
      }

      if(locationsList.length === 0)
      {
        jobsList[n].setAttribute("location-filter", "europe americas asia middle-east africa oceania");
      }
      else
      {
        locationsList = locationsList.slice(0, locationsList.length-1);
        jobsList[n].setAttribute("location-filter", locationsList);
      }
    }
  }

  parseLocations();

  function init() {
    var queryFilter = urlParams.get('filter');
    var locationFilter = urlParams.get('location');

    revealFilters();

    if (domList) {
      var jobList = Array.from(domList.children);
/*
      if (filterSelect) {

        Array.from(filterSelect.options).forEach(function (el) {
          filters.push(el.value);
      });

        if (queryFilter) {
          filterSelect.options.selectedIndex = filters.indexOf(queryFilter);
          updateFilterBy(filterSelect.options[filterSelect.options.selectedIndex].value);
          //filterJobs(filterBy, jobList);
          updateNoResultsMessage();
        }
        
        filterSelect.addEventListener("change", function () {
          if (!(sortSelect.options.selectedIndex === 0)) {
            sortSelect.options.selectedIndex = 0;
          }
          updateFilterBy(filterSelect.options[filterSelect.options.selectedIndex].value);
          //filterJobs(filterBy, jobList);
          updateURL(filterBy);
          updateNoResultsMessage();
        });

      }

      if (locationSelect) {
        Array.from(locationSelect.options).forEach(function (el) {
          locationFilters.push(el.value);
        });

        if (locationFilter) {
          locationSelect.options.selectedIndex = filters.indexOf(locationFilter);
          updateLocationFilterBy(locationSelect.options[locationSelect.options.selectedIndex].value);
          updateNoResultsMessage();
        }

        locationSelect.addEventListener("change", function () {
          if (!(sortSelect.options.selectedIndex === 0)) {
            sortSelect.options.selectedIndex = 0;
          }
          updateLocationFilterBy(locationSelect.options[locationSelect.options.selectedIndex].value);
          ///filterJobs(filterBy, jobList);
          updateURL(filterBy);
          updateNoResultsMessage();
        });
      }

      if(filterSelect || locationSelect)
      {
        filterJobs(filterBy, jobList);
      }
*/

      if(filterSelect && locationSelect) {
        getOptions(filters);
        getOptions(locationFilters);
        
        if(queryFilter && locationFilter)
        {
          filterSelect = updateOptions(filterSelect, queryFilter, filters, "filter");
          locationSelect = updateOptions(locationSelect, locationFilter, locationFilters, "location");
          filterJobs(filterBy, jobList);
          filterSelect = getEventListener(filterSelect, sortSelect, "filter", filterBy, jobList);
          locationSelect = getEventListener(locationSelect, sortSelect, "location", filterBy, jobList);
        }
        else if(queryFilter && !locationFilter)
        {
          filterSelect = updateOptions(filterSelect, queryFilter, filters, "filter");
          filterJobs(filterBy, jobList);
          filterSelect = getEventListener(filterSelect, sortSelect, "filter", filterBy, jobList);

        }
        else if(!queryFilter && locationFilter)
        {
          locationSelect = updateOptions(locationSelect, locationFilter, locationFilters, "location");
          filterJobs(filterBy, jobList);
          locationSelect = getEventListener(locationSelect, sortSelect, "location", filterBy, jobList);
        }
      }
      else if(filterSelect && !locationSelect) {
        getOptions(filters);

        if(queryFilter)
        {
          filterSelect = updateOptions(filterSelect, queryFilter, filters, "filter");
          filterJobs(filterBy, jobList);
          filterSelect = getEventListener(filterSelect, sortSelect, "filter", filterBy, jobList);
        }
      }
      else if(!filterSelect && locationSelect) {
        getOptions(locationFilters);

        if(locationFilter)
        {
          locationSelect = updateOptions(locationSelect, locationFilter, locationFilters, "location");
          filterJobs(filterBy, jobList);
          locationSelect = getEventListener(locationSelect, sortSelect, "location", filterBy, jobList);
        }
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
      if (filterBy.filterText === "All" && filterBy.location === "all") {
        if (node.classList.contains("u-hide")) {
          node.classList.remove("u-hide");
        }
        numberOfJobsDisplayed = domList.childElementCount;
      } else {
        if (node.dataset[filterBy.filterName].includes(filterBy.filterText) && node.getAttribute("location-filter").includes(filterBy.location)) {
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
    switch (filter) {
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

    urlParams.set('filter', filterBy.filterValue);
    urlParams.set('location', filterBy.location);

    var url = baseURL + '?' + urlParams.toString() + '#available-roles';

    window.history.pushState({}, "", url);
  }

  function getOptions(array)
  {
    Array.from(filterSelect.options).forEach(function (el) {
      array.push(el.value);
    });
  }

  function updateOptions(filterSelect, queryFilter, filters, type)
  {
    filterSelect.options.selectedIndex = filters.indexOf(queryFilter);
    if(type === "filter")
    {
      updateFilterBy(filterSelect.options[filterSelect.options.selectedIndex].value);
    }
    else if(type === "location")
    {
      updateLocationFilterBy(filterSelect.options[filterSelect.options.selectedIndex].value);
    }
    //filterJobs(filterBy, jobList);
    updateNoResultsMessage();
    return filterSelect;
  }

  function getEventListener(filterSelect, sortSelect, type, filterBy, jobList)
  {
    filterSelect.addEventListener("change", function () {
    if (!(sortSelect.options.selectedIndex === 0)) {
      sortSelect.options.selectedIndex = 0;
    }
    if(type === "filter")
    {
      updateFilterBy(filterSelect.options[filterSelect.options.selectedIndex].value);
    }
    else if(type === "location")
    {
      updateLocationFilterBy(filterSelect.options[filterSelect.options.selectedIndex].value);
    }
    filterJobs(filterBy, jobList);
    updateURL(filterBy);
    updateNoResultsMessage();
    return filterSelect;
    });
  }

  init();
})();

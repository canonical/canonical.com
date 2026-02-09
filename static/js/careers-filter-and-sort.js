(function () {
  const urlParams = new URLSearchParams(window.location.search);
  const baseURL = window.location.origin + window.location.pathname;
  const search_input = document.querySelector(".js-careers__search-input");
  const domList = document.querySelector(".js-job-list");
  /** @type {NodeListOf<HTMLInputElement>} */
  const departmentFilters = document.querySelectorAll(".js-filter");
  /** @type {NodeListOf<HTMLInputElement>} */
  const locationFilters = document.querySelectorAll(".js-filter--location");
  const noResults = document.querySelector(".js-filter__no-results");
  const jobContainer = document.querySelector(".js-filter-jobs-container");
  /** @type {HTMLInputElement | null} */
  const searchBox = document.querySelector(".js-careers__search-input");
  const showMoreButton = document.querySelector("#show-20-more");
  const showAllButton = document.querySelector("#show-all");
  const showMoreIncrement = 20;
  let jobList = [];
  let filteredJobList = [];
  let limit = showMoreIncrement;
  let selectedDeptFilters = [];
  let selectedLocationFilters = [];

  // Show search and filter functionality if JS is available
  function revealSearch() {
    const searchForm = document.querySelector(".js-search-jobs-form");
    if (searchForm) {
      searchForm.classList.remove("u-hide");
    }
  }
  var numberOfJobsDisplayed = 0;

  // Read data-location property and parse locations into well-defined categories
  function parseLocations(location, filters) {
    const regions = {
      emea: [
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
        "boston",
      ],
      apac: ["apac", "taiwan", "taipei", "beijing", "china", "worldwide"],
    };

    // format job location string
    local = location.toLowerCase().split("-").pop().split(",");

    //check if job location matches a location in filtered region(s)
    for (let i = 0; i < filters.length; i++) {
      let regionKey = regions[filters[i].toLowerCase()];
      for (let j = 0; j < local.length; j++) {
        if (Object.values(regionKey).includes(local[j].trim())) {
          return 1;
        }
      }
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

  function checkUrlFilters(jobList) {
    const loadedDeptFiters = urlParams.getAll("filter");
    if (loadedDeptFiters) {
      // If the page is loaded with inital URL parameters, change the default form selection and filter the results to reflect this

      for (let i = 0; i < loadedDeptFiters.length; i++) {
        deptFilter = loadedDeptFiters[i];
        inputElement = document.getElementsByName(deptFilter)[0];
        if (inputElement) {
          inputElement.checked = true;
        }
      }
    }

    const loadedLocationFilters = urlParams.getAll("location");
    if (loadedLocationFilters) {
      for (let i = 0; i < loadedLocationFilters.length; i++) {
        locationFilter = loadedLocationFilters[i];
        inputElement = document.getElementsByName(locationFilter)[0];
        if (inputElement) {
          inputElement.checked = true;
        }
      }
    }

    filterJobs(loadedDeptFiters, loadedLocationFilters, jobList);
  }

  function filtersListener(el, jobList) {
    if (el.type === "checkbox") {
      selectedDeptFilters = Array.from(departmentFilters)
        .filter((el) => el.checked)
        .map((el) => el.name);
      selectedLocationFilters = Array.from(locationFilters)
        .filter((el) => el.checked)
        .map((el) => el.name);

      filterJobs(selectedDeptFilters, selectedLocationFilters, jobList);
      updateFilterParams(selectedDeptFilters, selectedLocationFilters);
    }
  }

  function init() {
    revealSearch();
    revealFilters();
    if (searchBox) {
      populateTextbox();
    }

    if (domList) {
      jobList = Array.from(domList.children);
    }

    if (jobList.length > 0) {
      initShowMore();
      checkUrlFilters(jobList);

      if (departmentFilters) {
        departmentFilters.forEach(
          (/** @type {HTMLInputElement} */ el) =>
            (el.onclick = function () {
              filtersListener(el, jobList);
            })
        );
      }

      if (locationFilters) {
        locationFilters.forEach(
          (/** @type {HTMLInputElement} */ el) =>
            (el.onclick = function () {
              filtersListener(el, jobList);
            })
        );
      }
    } else {
      updateNoResultsMessage();
      showButtons(jobList);
    }
  }

  function initShowMore() {
    filteredJobList = jobList;
    showButtons(filteredJobList);
    showJobs(filteredJobList);
    handleShowMoreClick();
    handleShowAllClick();
  }

  function updateTotalNumber(shownJobs, jobList) {
    let totalResultsElement = document.querySelector("#total-results");
    if (shownJobs.length > 0) {
      totalResultsElement.innerHTML = `${shownJobs.length} of ${jobList.length} roles`;
    } else {
      totalResultsElement.innerHTML = "";
    }
  }

  function showButtons(shownJobs) {
    let listLength = shownJobs.length;

    if (listLength <= limit) {
      showMoreButton.classList.add("u-hide");
      showAllButton.classList.add("u-hide");
    } else if (listLength > limit && listLength < limit + showMoreIncrement) {
      showMoreButton.classList.add("u-hide");
      showAllButton.classList.remove("u-hide");
    } else {
      showMoreButton.classList.remove("u-hide");
      showAllButton.classList.add("u-hide");
    }
  }

  function showJobs(jobs) {
    const jobsToShow = jobs.slice(0, limit);
    const jobsToHide = jobs.slice(limit);
    updateTotalNumber(jobsToShow, jobs);
    numberOfJobsDisplayed = jobsToShow.length;
    updateNoResultsMessage();

    jobList.forEach((job) => {
      job.classList.add("u-hide");
    });

    jobsToShow.forEach((job) => {
      job.classList.remove("u-hide");
    });

    jobsToHide.forEach((job) => {
      job.classList.add("u-hide");
    });
  }

  function handleShowMoreClick() {
    showMoreButton.addEventListener("click", function () {
      limit = limit + showMoreIncrement;
      showJobs(filteredJobList);
      showButtons(filteredJobList);
    });
  }

  function handleShowAllClick() {
    showAllButton.addEventListener("click", function () {
      limit = filteredJobList.length;
      showJobs(filteredJobList);
      showButtons(filteredJobList);
    });
  }

  // Show filters if JS is available
  function revealFilters() {
    var filterForm = document.querySelector(".js-filter-form");
    if (filterForm) {
      filterForm.classList.remove("u-hide");
    }
  }

  function filterJobs(selectedDeptFilters, selectedLocalFilters, jobList) {
    numberOfJobsDisplayed = domList.childElementCount;
    let jobsToShow = [];
    jobList.forEach((job) => {
      let departments = job.departments;
      let jobLocation = job.dataset.location;
      let matchingDepartments = selectedDeptFilters.filter((value) =>
        departments.includes(value)
      );

      // check if we are searching based on department
      if (selectedDeptFilters.length) {
        // then check if we have department matches and location filters
        if (matchingDepartments.length && selectedLocalFilters.length) {
          // filter the department matches based on location
          if (
            matchingDepartments.length &&
            parseLocations(jobLocation, selectedLocalFilters)
          ) {
            jobsToShow.push(job);
          }
          // otherwise just filter by department matches
        } else if (matchingDepartments.length && !selectedLocalFilters.length) {
          jobsToShow.push(job);
        }
        // otherwise filter based only on location
      } else if (selectedLocalFilters.length) {
        if (
          parseLocations(jobLocation, selectedLocalFilters) &&
          !jobsToShow.includes(job)
        ) {
          jobsToShow.push(job);
        }
      }
    });

    if (selectedDeptFilters.length || selectedLocalFilters.length) {
      filteredJobList = jobsToShow;
      showJobs(filteredJobList);
      showButtons(filteredJobList);
    } else {
      limit = showMoreIncrement;
      filteredJobList = jobList;
      showJobs(jobList);
      showButtons(jobList);
    }
  }

  // Display no results message
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

  // handle search input clear, retain existing filters
  search_input.addEventListener("input", (e) => {
    /** @type {HTMLInputElement} */
    const target = e.target;
    search_term = target.value;
    updateURL();
  });

  function updateURL() {
    if (search_term == "" && window.location.pathname === "/careers/all") {
      urlParams.delete("search");
      window.location = `${baseURL}/?${urlParams.toString()}`;
    }
  }

  function updateFilterParams(selectedDeptFilters, selectedLocationFilters) {
    // if url has filter param but filter array is empty, remove filter from url
    if (urlParams.has("filter") && selectedDeptFilters.length == 0) {
      urlParams.delete("filter");
    } else {
      if (selectedDeptFilters.length > 0) {
        // set first filter
        urlParams.set("filter", selectedDeptFilters[0]);
        // append if more filters
        for (let i = 1; i < selectedDeptFilters.length; i++) {
          urlParams.append("filter", selectedDeptFilters[i]);
        }
      }
    }

    // if url has location param but location array is empty, remove location filter from url
    if (urlParams.has("location") && selectedLocationFilters.length == 0) {
      urlParams.delete("location");
    } else {
      if (selectedLocationFilters.length > 0) {
        // set first filter
        urlParams.set("location", selectedLocationFilters[0]);
        // append if more filters
        for (let i = 1; i < selectedLocationFilters.length; i++) {
          urlParams.append("location", selectedLocationFilters[i]);
        }
      }
    }

    var url = baseURL + "?" + urlParams.toString();
    window.history.pushState({}, "", url);
  }
  window.addEventListener("DOMContentLoaded", (event) => {
    init();
  });
})();

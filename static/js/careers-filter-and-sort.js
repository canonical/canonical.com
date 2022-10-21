(function () {
  const urlParams = new URLSearchParams(window.location.search);
  const domList = document.querySelector(".js-job-list");
  const departmentFilters = document.querySelectorAll(".js-filter");
  const noResults = document.querySelector(".js-filter__no-results");
  const jobContainer = document.querySelector(".js-filter-jobs-container");
  const locationFilters = document.querySelectorAll(".js-filter--location");
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
        "boston"
      ],
      apac: [
        "apac",
        "taiwan",
        "taipei",
        "beijing",
        "china",
        "worldwide"
      ],
    };

    // format job location string
    local = location.toLowerCase().split('-').pop().split(',');

    //check if job location matches a location in filtered region(s)
    for (let i = 0; i < filters.length; i++) {
      let regionKey = regions[filters[i].toLowerCase()]
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

  function checkUrlFilters(selectedDeptFilters, selectedLocationFilters, jobList) {
    if (urlParams.has("filter")) {
      // If the page is loaded with inital URL parameters, change the default form selection and filter the results to reflect this
      let loadedDeptFiters = urlParams.getAll("filter");

      for (let i = 0; i < loadedDeptFiters.length; i++){
        deptFilter = loadedDeptFiters[i]
        inputElement = document.getElementsByName(deptFilter)[0];

        inputElement.onclick = function(){departmentFiltersListener(inputElement, selectedDeptFilters, selectedLocationFilters,jobList)}
        inputElement.click()
      }
    }

    if (urlParams.has("location")) {
      let loadedLocationFilters = urlParams.getAll("location");

      for (let i = 0; i < loadedLocationFilters.length; i++){
        locationFilter = loadedLocationFilters[i]
        inputElement = document.getElementsByName(locationFilter)[0];

        inputElement.onclick = function(){locationListener(inputElement, selectedDeptFilters, selectedLocationFilters,jobList)}
        inputElement.click()
      }
    }
  };

  function departmentFiltersListener(el, selectedDeptFilters, selectedLocationFilters,jobList) {
    let filterName = el.name;

    if (el.checked){
      selectedDeptFilters.push(filterName)
      filterJobs(selectedDeptFilters, selectedLocationFilters, jobList);
      updateURL(selectedDeptFilters, selectedLocationFilters)
    } else {
      let index = selectedDeptFilters.indexOf(filterName)
      if (index > -1) {
        selectedDeptFilters.splice(index, 1)
      }
      filterJobs(selectedDeptFilters, selectedLocationFilters ,jobList);
      updateURL(selectedDeptFilters, selectedLocationFilters);
    }
  }

  function locationListener (el, selectedDeptFilters, selectedLocationFilters,jobList){
    let locationName = el.name;

    if (el.checked){
      selectedLocationFilters.push(locationName)
      filterJobs(selectedDeptFilters, selectedLocationFilters, jobList);
      updateURL(selectedDeptFilters, selectedLocationFilters);
    } else {
      let index = selectedLocationFilters.indexOf(locationName)
      if (index > -1) {
        selectedLocationFilters.splice(index, 1)
      }
      filterJobs(selectedDeptFilters, selectedLocationFilters, jobList);
      updateURL(selectedDeptFilters, selectedLocationFilters);
    }
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
      jobList = Array.from(domList.children);
    }

    if (jobList.length > 0) {
      initShowMore();
      checkUrlFilters(selectedDeptFilters, selectedLocationFilters, jobList)

      if (departmentFilters) {
        departmentFilters.forEach(el => el.onclick = function(){departmentFiltersListener(el, selectedDeptFilters, selectedLocationFilters,jobList)})
      }

      if (locationFilters) {
        locationFilters.forEach(el => el.onclick = function(){locationListener(el, selectedDeptFilters, selectedLocationFilters,jobList)})
      }
    } else {
      updateNoResultsMessage()
      showButtons(jobList)
    }
  }

  function initShowMore() {
    filteredJobList = jobList;
    showButtons(filteredJobList)
    showJobs(filteredJobList);
    handleShowMoreClick();
  }

  function updateTotalNumber(shownJobs, jobList) {
    let totalResultsElement = document.querySelector("#total-results");

    totalResultsElement.innerHTML = `${shownJobs.length} of ${jobList.length} roles`;
  }

  function showButtons(shownJobs){
    let listLength = shownJobs.length;

    if (listLength <= limit){
      showMoreButton.classList.add('u-hide');
      showAllButton.classList.add('u-hide');
    } else if (listLength > limit && listLength < (limit + showMoreIncrement)) {
      showMoreButton.classList.add('u-hide');
      showAllButton.classList.remove('u-hide');
    } else {
      showMoreButton.classList.remove('u-hide');
      showAllButton.classList.add('u-hide');
    }
  }

  function showJobs(jobs) {
    const jobsToShow = jobs.slice(0, limit)
    const jobsToHide = jobs.slice(limit)
    updateTotalNumber(jobsToShow, jobs)

    jobList.forEach(job => {
      job.classList.add('u-hide');
    })

    jobsToShow.forEach(job => {
      job.classList.remove('u-hide');
    });

    jobsToHide.forEach(job => {
      job.classList.add('u-hide');
    })
  }

  function handleShowMoreClick() {
    showMoreButton.addEventListener("click", function(){
      limit = limit + showMoreIncrement;
      showJobs(filteredJobList);
      showButtons(filteredJobList)
    })
  }

  function handleShowAllClick() {
    showAllButton.addEventListener("click", function(){
      limit = filteredJobList.length;
      showJobs(filteredJobList);
      showButtons(filteredJobList);
    })
  }

  // Show filters if JS is available
  function revealFilters() {
    var filterForm = document.querySelector(".js-filter-form");
    if (filterForm) {
      filterForm.classList.remove("u-hide");
    }
  }

  function filterJobs(selectedDeptFilters, localFilters, jobList){
    numberOfJobsDisplayed = domList.childElementCount;
    let jobsToShow = [];

    jobList.forEach(job => {
      let jobSector = job.dataset.sector;
      let jobLocation = job.dataset.location;

      if (selectedDeptFilters.length > 0 && localFilters.length > 0) {
        if (selectedDeptFilters.includes(jobSector) && parseLocations(jobLocation, localFilters)){
          jobsToShow.push(job)
        }
      } else {
        //filter by dept
        if (selectedDeptFilters.length > 0){
          if (selectedDeptFilters.includes(jobSector)){
            jobsToShow.push(job)
          }
        }
        // filter by location
        if (localFilters.length > 0){
          if (parseLocations(jobLocation, localFilters) && !jobsToShow.includes(job)){
            jobsToShow.push(job)
          }
        }
      }
    });

    if (selectedDeptFilters.length || localFilters.length) {
      filteredJobList = jobsToShow;
      showJobs(filteredJobList)
      showButtons(filteredJobList)
      handleShowAllClick(filteredJobList)
    } else {
      limit = showMoreIncrement;
      showJobs(jobList)
      showButtons(jobList)
      handleShowAllClick(jobList)
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

  function updateURL(selectedDeptFilters, selectedLocationFilters) {
    var baseURL = window.location.origin + window.location.pathname;

    // if url has filter param but filter array is empty, remove filter from url
    if (urlParams.has("filter") && selectedDeptFilters.length == 0){
      urlParams.delete("filter");
    } else {
      if (selectedDeptFilters.length > 0){
      // set first filter
        urlParams.set("filter", selectedDeptFilters[0])
        // append if more filters
        for (let i = 1; i < selectedDeptFilters.length; i++){
          urlParams.append("filter", selectedDeptFilters[i]);
        }
      }
    }

    // if url has location param but location array is empty, remove location filter from url
    if (urlParams.has("location") && selectedLocationFilters.length == 0){
      urlParams.delete("location");
    } else {
      if (selectedLocationFilters.length > 0){
      // set first filter
        urlParams.set("location", selectedLocationFilters[0])
        // append if more filters
        for (let i = 1; i < selectedLocationFilters.length; i++){
          urlParams.append("location", selectedLocationFilters[i]);
        }
      }
    }

    var url = baseURL + "?" + urlParams.toString();
    window.history.pushState({}, "", url);
  }
    window.addEventListener('DOMContentLoaded', (event) => {
      init();
    })
  })();

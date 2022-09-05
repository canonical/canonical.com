(function () {
  const urlParams = new URLSearchParams(window.location.search);
  const domList = document.querySelector(".js-job-list");
  const departmentFilters = document.querySelectorAll(".js-filter");
  const noResults = document.querySelector(".js-filter__no-results");
  const jobContainer = document.querySelector(".js-filter-jobs-container");
  const locationSelect = document.querySelector(".js-filter--location");
  const tempLocationSelect = document.querySelectorAll(".js-filter--location");
  const searchBox = document.querySelector(".js-careers__search-input");
  const showMoreButton = document.querySelector("#show-20-more")
  const showAllButton = document.querySelector("#show-all")
  const showMoreIncrement = 20;
  let jobList = [];
  let filteredJobList = [];
  let limit = showMoreIncrement;
  
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
  function parseLocations(location, filters) {
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
        "boston"
      ],
      asia: ["apac", "taiwan", "taipei", "beijing", "china", "worldwide"],
      "middle-east": ["emea", "worldwide"],
      africa: ["emea", "worldwide"],
      oceania: ["apac", "worldwide"],
    };
    
    // format job location string 
    local = location.toLowerCase().split('-').pop().split(',');

    //check if job location matches a location in filtered region(s)
    for (let i = 0; i < filters.length; i++){
      let regionKey = regions[filters[i]]
      for (let j =0; j < local.length; j++) {
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

      let newOptions = [];
      departmentFilters.forEach(el => newOptions.push(el.name));
      let storedDeptFilters = []
      let storedLocationFilters = []

      if (departmentFilters) {
        // Get list of options from the HTML form
        var filterOptions = [];
        departmentFilters.forEach(el => filterOptions.push(el.name));

        // if (urlParams.has("filter")) {
        //   // If the page is loaded with inital URL parameters, change the default form selection and filter the results to reflect this
        //   var filterValue = urlParams.get("filter");
        //   for (let n = 0; n < filterOptions.length; n++) {
        //     if (filterOptions[n] === filterValue) {
        //       filterSelect.options.selectedIndex = n;
        //       break;
        //     }
        //   }
        // }

      
        departmentFilters.forEach(el => el.onclick = function(){departmentFiltersListener(el, storedDeptFilters)})
        
        // Add filter to stored array if checked, remove it if unchcecked. Pass array to job filter and update URL
        function departmentFiltersListener(el, storedDeptFilters) {
          if (el.checked){
            storedDeptFilters.push(el.name)
            updateURL(el.name, storedDeptFilters);
            // updateNoResultsMessage();
          } else {
            let index = storedDeptFilters.indexOf(el.name)
            if (index > -1) {
              storedDeptFilters.splice(index, 1)
            }             
          }
          tempFilterJobs(storedDeptFilters, storedLocationFilters ,jobList);
        }
      }

      if (tempLocationSelect) {
        // Get list of options from the HTML form
        var locationOptions = [];
        tempLocationSelect.forEach(el => locationOptions.push(el.name));

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

        
        // Add filter to stored array if checked, remove it if unchcecked. Pass array to job filter and update URL
        tempLocationSelect.forEach(el => el.onclick = function(){locationListener(el, storedLocationFilters)})
        function locationListener (el, storedLocationFilters){
          let filterName = el.name.toLowerCase();
          if (el.checked){
            storedLocationFilters.push(filterName)
            // updateURL(el.name, storedLocationFilters);
          } else {
            let index = storedLocationFilters.indexOf(filterName)
            if (index > -1) {
              storedLocationFilters.splice(index, 1)
              // updateURL(el.name, storedLocationFilters);
            }           
          }
          tempFilterJobs(storedDeptFilters, storedLocationFilters, jobList);
        }
      }

      tempFilterJobs(storedDeptFilters, storedLocationFilters, jobList);
      updateNoResultsMessage();
    }
  }

  function initShowMore() {
    filteredJobList = jobList;
    //edit below for intial list
    console.log(filteredJobList.length)
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
    console.log(listLength, limit)
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
    // showButtons(jobsToShow)
    console.log(jobs.length, jobsToShow.length)
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
    })
  }

  function handleShowAllClick() {
    showAllButton.addEventListener("click", function(){
      limit = filteredJobList.length;
      showJobs(filteredJobList);
      console.log(filteredJobList, limit)
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

  function tempFilterJobs(deptFilters, localFilters, jobList){
    numberOfJobsDisplayed = domList.childElementCount;
    let jobsToShow = [];

    jobList.forEach(job => {
      let jobSector = job.dataset.sector;
      let jobLocation = job.dataset.location;

      if (deptFilters.length > 0 && localFilters.length > 0) {
        if (deptFilters.includes(jobSector) && parseLocations(jobLocation, localFilters)){
          jobsToShow.push(job)
        }
      } else {
        //filter by dept
        if (deptFilters.length > 0){
          if (deptFilters.includes(jobSector)){
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

    if (deptFilters.length || localFilters.length) {
      filteredJobList = jobsToShow;
      showJobs(filteredJobList)
      showButtons(filteredJobList)
      handleShowAllClick(filteredJobList)

    } else {
      limit = showMoreIncrement;
      showJobs(jobList)
      showButtons(jobList)
      handleShowAllClick(jobList)
      console.log("unfiltered")
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

  function updateURL(filterBy, filters) {
    // console.log(filters)
    var baseURL = window.location.origin + window.location.pathname;
    // console.log(filterBy)
    for (let i = 0; i < filters.length; i++){
      console.log("from loop",filters[i], baseURL)
      if (baseURL.includes(filters[i])){
        console.log("it does")
      } else {
        urlParams.append("filter", filters[i])
      }
    }
    // urlParams.set("filter", filterBy);
    urlParams.set("location", filterBy.location);

    var url = baseURL + "?" + urlParams.toString();
    console.log(url)
    window.history.pushState({}, "", url);
  }
    window.addEventListener('DOMContentLoaded', (event) => {
      init();
    })
  })();

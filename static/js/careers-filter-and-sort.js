(function () {
  const urlParams = new URLSearchParams(window.location.search);
  const domList = document.querySelector(".js-job-list");
  const departmentFilters = document.querySelectorAll(".js-filter");
  const noResults = document.querySelector(".js-filter__no-results");
  const jobContainer = document.querySelector(".js-filter-jobs-container");
  const locationSelect = document.querySelector(".js-filter--location");
  const tempLocationSelect = document.querySelectorAll(".js-filter--location");
  const searchBox = document.querySelector(".js-careers__search-input");
  const paginationButton = document.querySelector("#show-20-more")
  
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
      // console.log(regions[filters[i]], local, filters)
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

  function paginationControls(node, index, numberOfJobsDisplayed, limit) {
    console.log(index, limit, node)
    // first visit
    if (index > limit){
      if (!node.classList.contains("u-hide")) {
        node.classList.add("u-hide");
      }
      numberOfJobsDisplayed--;
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
      var jobList = Array.from(domList.children);

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
          if (el.checked){
            storedLocationFilters.push(el.name.toLowerCase())
            // updateURL(el.name, storedLocationFilters);
          } else {
            let index = storedLocationFilters.indexOf(el.name)
            if (index > -1) {
              storedLocationFilters.splice(index, 1)
            }           
          }
          tempFilterJobs(storedDeptFilters, storedLocationFilters, jobList);
        }
      }

      tempFilterJobs(storedDeptFilters, storedLocationFilters, jobList);
      updateNoResultsMessage();
    }
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
    console.log("before", numberOfJobsDisplayed)

    jobList.forEach(function (node, index) {
      let jobSector = node.dataset.sector;
      let jobLocation = node.dataset.location;
      let limit = 19;

      paginationButton.addEventListener("click", function(){
        limit = (limit * 2) +1 ;
        paginationControls(node, index, numberOfJobsDisplayed, limit)
      })
      
      if (deptFilters.length === 0 && localFilters.length === 0){
        
        paginationControls(node, index, numberOfJobsDisplayed, limit)
      } else {
        //filter by dept
        if (deptFilters.length > 0){
          if (deptFilters.includes(jobSector)){
            // if it was previously hidden, unhide it
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
        // filter by location 
        else if (localFilters.length > 0){
          if (parseLocations(jobLocation, localFilters)){
            console.log(node)
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
        // filter by both
      } 
    })

    console.log(numberOfJobsDisplayed)
  }

  function filterJobs(filterBy, jobList) {
    numberOfJobsDisplayed = domList.childElementCount;
    // jobList.forEach(job => checkFilters(job, filterBy))
    
    
    jobList.forEach(function (node) {
      console.log(node.dataset.sector, filterBy)

      // if there are no location or department filters
      if (filterBy.filterText === "All" && filterBy.location === "all") {
        if (node.classList.contains("u-hide")) {
          node.classList.remove("u-hide");
        }
        numberOfJobsDisplayed = domList.childElementCount;
      } 
      
      // if there are no location filters, but there are department filters
      else if (
        filterBy.filterValue !== "all" &&
        filterBy.location === "all"
      ) {
        if (node.dataset.sector == filterBy.filterText) {
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
          node.dataset.sector == filterBy.filterText &&
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

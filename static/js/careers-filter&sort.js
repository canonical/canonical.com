(function() {
  const filterSelect = document.querySelector(".js-filter");
  const sortSelect = document.querySelector(".js-sort");
  const domList = document.querySelector(".js-job-list");
  var jobList = Array.from(domList.children);

  filterSelect.addEventListener("change", function(e) {
    var filterBy = {};
    switch (filterSelect.options[filterSelect.options.selectedIndex].text) {
      case "Home based":
        filterBy.filterName = "office";
        filterBy.filterValue = "Home Based";
        break;
      case "Office based":
        filterBy.filterName = "office";
        filterBy.filterValue = "Office Based";
        break;
      case "Management":
        filterBy.filterName = "management";
        filterBy.filterValue = "True";
        break;
      case "Full-time":
        filterBy.filterName = "employment";
        filterBy.filterValue = "Full-time";
        break;
      case "Part-time":
        filterBy.filterName = "employment";
        filterBy.filterValue = "Part-time";
    }
    filterJobs(filterBy);  
  });

  sortSelect.addEventListener("change", function (e) {
    var sortBy = "date";
    switch (sortSelect.options[sortSelect.options.selectedIndex].text) {
      case "Date":
        sortBy = "date";
        break;
      case "Location":
        sortBy = "location";
        break;
      case "Job sector":
        sortBy = "sector";
    }
    jobList.sort((a, b) => a.dataset[sortBy] !== b.dataset[sortBy] ? a.dataset[sortBy] < b.dataset[sortBy] ? -1 : 1: 0);
    if (sortBy === "date") {
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

  function filterJobs(filterBy) {
    jobList.forEach(function(node) {
      if (!filterBy) {
        if (node.classList.contains("u-hide")) {
          node.classList.remove("u-hide");
        }
      } else {
        if (filterBy.filterValue === node.dataset[filterBy.filterName]) {
          if (node.classList.contains("u-hide")) {
            node.classList.remove("u-hide");
          }
        } else {
          if (!node.classList.contains("u-hide")) {
            node.classList.add("u-hide");
          }
        }
      }
    });
  };
})();

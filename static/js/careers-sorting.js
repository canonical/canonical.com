(function() {
  const sortSelect = document.querySelector(".js-sort");
  const domList = document.querySelector(".js-sort-list");
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
    var jobList = Array.from(domList.children);
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
})();
(function() {

  var filters = [];

  function init() {
    revealSearch();

    var inputNode = document.querySelector(".p-find-a-partner__search-input");
    inputNode.addEventListener("keyup", searchHandler);

    var checkboxes = document.querySelectorAll(".p-find-a-partner__filter");
    checkboxes.forEach(function(checkbox) {
      checkbox.addEventListener("change", filter);
    });

    populateCheckboxes();
    populateTextbox();
  }

  function matchesExist() {
    var numberOfPartners = document.querySelectorAll(
      ".p-find-a-partner__partner"
    ).length;
    var numberOfHidden = document.querySelectorAll(
      ".p-find-a-partner__partner.u-hide"
    ).length;
    if (numberOfHidden === numberOfPartners) {
      return false;
    } else {
      return true;
    }
  }

  function updateNoResultsMessage() {
    var noResults = document.querySelector(".p-find-a-partner__no-results");
    if (matchesExist()) {
      noResults.classList.add("u-hide");
    } else {
      noResults.classList.remove("u-hide");
    }
  }

  function searchHandler(e) {
    var query = e.target.value.toLowerCase();
    search(query);
  }

  function search(query) {
    var partners = document.querySelectorAll(
      ".p-find-a-partner__partner:not(.js-filtered)"
    );

    partners.forEach(function(node) {
      node.classList.add("u-hide");
      var searchText = node.getAttribute("data-searchText").toLowerCase();
      if (searchText.includes(query)) {
        node.classList.remove("u-hide");
      }
    });
    updateNoResultsMessage();
  }

  function filter(e) {
    var checkbox = e.target;
    var checked = checkbox.checked;
    var attributeName = checkbox.id;
    updateFilter(attributeName, checked);
    updateNoResultsMessage();
  }

  //Adds the provided filter and filters the results accordingly
  function updateFilter(name, add) {
    filters[name] = add;
    partners = document.querySelectorAll(".p-find-a-partner__partner");
    partners.forEach(function(node) {
      node.classList.add("u-hide", "js-filtered");

      dataFilter = node.getAttribute("data-filter");
      for (var name in filters) {
        if (filters[name] == true && dataFilter.indexOf(name) != -1) {
          node.classList.remove("u-hide", "js-filtered");
        }
      }
    });

    if (filters.indexOf(true) == -1) {
      if (
        partners.length ==
        document.querySelectorAll(".p-find-a-partner__partner.u-hide").length
      ) {
        partners.forEach(function(node) {
          node.classList.remove("u-hide");
        });
      }
    }
  }

  //Get specified query param
  function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
      results = regex.exec(location.search);
    return results == null
      ? ""
      : decodeURIComponent(results[1].replace(/\+/g, " "));
  }

  //check any checkboxes that match URL queries
  function populateCheckboxes() {
    //get URL query params
    var queryParams = (function(queryString) {
      if (queryString == "") return {};
      var returnParams = {};
      for (var i = 0; i < queryString.length; ++i) {
        var queryArray = queryString[i].split("=", 2);
        if (
          Object.prototype.toString.call(returnParams[queryArray[0]]) !==
          "[object Array]"
        ) {
          returnParams[queryArray[0].toLowerCase()] = new Array();
        }
        if (queryArray.length == 1) {
          //query param is just a key
          returnParams[queryArray[0]] = "";
        } else {
          //query param is key/value
          var rawQueryParam = decodeURIComponent(queryArray[1]);
          var cleanQueryParam = rawQueryParam
            .replace("/", "")
            .replace(/\W+/g, "-")
            .toLowerCase(); //sanitise raw input
          returnParams[queryArray[0].toLowerCase()].push(cleanQueryParam);
        }
      }
      return returnParams;
    })(window.location.search.substr(1).split("&"));

    //check any appropriate checkboxes
    for (var key in queryParams) {
      for (var i = 0; i < queryParams[key].length; ++i) {
        var checkboxObject = document.querySelector(
          "#" + key + "-" + queryParams[key][i]
        );
        if (checkboxObject != null) {
          checkboxObject.setAttribute("checked", "checked");
          updateFilter(key + "-" + queryParams[key][i], true);
          document.querySelector("#" + key).classList.add("open");
        }
      }
    }
  }

  function populateTextbox() {
    var searchbox = document.querySelector(".p-find-a-partner__search-input");
    var searchText = getParameterByName("search");
    if (searchbox && searchText) {
      searchbox.focus();
      searchbox.value = searchText;
      search(searchText);
    }
  }

  function revealSearch() {
    var searchForm = document.querySelector(".p-strip--light.is-shallow.u-hide");
    searchForm.classList.remove("u-hide");
  }

  init();

})();

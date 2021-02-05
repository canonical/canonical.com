(function () {
  // Mapbox api
  const API_KEY =
    "pk.eyJ1IjoiY2Fub25pY2FsLXdlYnRlYW0iLCJhIjoiY2swZ3M0Y2tpMDNvMzNubGo1NG9pajZqMiJ9.v8qNlzrS4_gI5pJZQTAFaQ";
  const url = "https://api.mapbox.com/geocoding/v5/mapbox.places/";

  var numberOfEducations = 0;

  const addEducationButton = document.querySelector(".js-add-education");
  const locateMeButton = document.querySelector(".js-locate-me");
  const locateMeError = document.querySelector(".js-locate-error");
  const locationLabel = document.querySelector(".js-location");
  const educationContainer = document.querySelector(".education-container");
  const schoolsList = document.querySelector(".js-school-0");

  var defaultDegreeList = [];
  var defaultDisciplineList = [];

  window.onload = async function () {
    defaultDegreeList = await getDataFromGreenhouseApi("degrees", "");
    defaultDisciplineList = await getDataFromGreenhouseApi("disciplines", "");
    populateDegreeList("#degree-0", defaultDegreeList);
    populateDisciplineList("#discipline-0", defaultDisciplineList);
  };

  async function populateDegreeList(degreeId, degrees) {
    const datalistDegreeElement = document.querySelector(degreeId);
    if (!degrees) {
      degrees = await getDataFromGreenhouseApi("degrees", "");
    }
    var degreeList = "";
    degrees.forEach((degree) => {
      degreeList += `<option value="${degree.text}" />`;
    });
    if (datalistDegreeElement) {
      datalistDegreeElement.innerHTML = degreeList;
    }
  }

  async function populateDisciplineList(disciplineId, disciplines) {
    const datalistDisciplineElement = document.querySelector(disciplineId);
    if (!disciplines) {
      disciplines = await getDataFromGreenhouseApi("disciplines", "");
    }
    var disciplineList = "";
    disciplines.forEach((discipline) => {
      disciplineList += `<option value="${discipline.text}" />`;
    });
    if (datalistDisciplineElement) {
      datalistDisciplineElement.innerHTML = disciplineList;
    }
  }

  async function getDataFromGreenhouseApi(category, term) {
    var url = "";
    if (term && term != "") {
      url = `https://boards-api.greenhouse.io/v1/boards/Canonical/education/${category}?term=${term}`;
    } else {
      url = `https://boards-api.greenhouse.io/v1/boards/Canonical/education/${category}`;
    }
    response = await fetch(url);
    if (response.ok) {
      const data = await response.json();
      return data.items;
    } else {
      console.log("HTTP-Error: " + response.status);
    }
  }

  function addEducationInput(n) {
    const educationInput = document.createElement("div");
    educationInput.setAttribute("data-education", n);
    educationInput.innerHTML = `  
      <hr/>
      <a href="#" class="js-remove-education">
        <i class="p-icon--close" style="float: right;"></i>
      </a>
      <label for="school-${n}">School</label>
      <input list="school-${n}" name="school-${n}" type="text" class="js-school-${n}">
      <datalist id="school-${n}">
      </datalist>
      <label for="degree-${n}">Degree</label>
      <input list="degree-${n}" name="degree-${n}" type="text" class="js-degree-${n}">
      <datalist id="degree-${n}">
      </datalist>
      <label for="discipline-${n}">Discipline</label>
      <input list="discipline-${n}" name="discipline-${n}" type="text" class="js-dicipline-${n}">
      <datalist id="discipline-${n}">
      </datalist>
      <div class="p-form--inline">
        <div class="p-form__group">
          <label class="p-form__label">Start date</label>
          <div class="p-form__control u-clearfix">
            <input placeholder="MM" id="start-month-${n}" name="start-month-${n}" type="text" class="p-form__control">
          </div>
          <div class="p-form__control u-clearfix">
            <input placeholder="YYYY" id="start-year-${n}" name="start-year-${n}" type="text" class="p-form__control">
          </div>
        </div>
      </div>
      <div class="p-form--inline">
        <div class="p-form__group">
          <label class="p-form__label">End date</label>
          <div class="p-form__control u-clearfix">
            <input placeholder="MM" id="end-month-${n}" name="end-month-${n}" type="text" class="p-form__control">
          </div>
          <div class="p-form__control u-clearfix">
            <input placeholder="YYYY" id="end-year-${n}" name="end-year-${n}" type="text" class="p-form__control">
          </div>
        </div>
      </div>`;
    educationContainer.appendChild(educationInput);
  }

  if (schoolsList) {
    schoolsList.addEventListener(
      "input",
      debounce(async (e) => {
        const datalistElement = document.querySelector("#school-0");
        var schools = [];
        if (e.target.value !== "") {
          schools = await getDataFromGreenhouseApi("schools", e.target.value);
        }
        var list = "";
        schools.forEach((school) => {
          list += `<option value="${school.text}" />`;
        });
        datalistElement.innerHTML = list;
      }, 350)
    );
  }

  if (addEducationButton) {
    addEducationButton.addEventListener("click", () => {
      numberOfEducations++;
      addEducationInput(numberOfEducations);
      // Add click event listener to the "remove education" button
      const removeEducationButtons = document.querySelectorAll(
        ".js-remove-education"
      );
      if (removeEducationButtons && removeEducationButtons.length > 0) {
        removeEducationButtons[
          removeEducationButtons.length - 1
        ].addEventListener("click", (e) => {
          e.preventDefault();
          const educationToBeRemoved = e.target.closest("div");
          educationToBeRemoved.parentNode.removeChild(educationToBeRemoved);
        });
      }
      // Populate new added input datalists
      populateDegreeList(`#degree-${numberOfEducations}`, defaultDegreeList);
      populateDisciplineList(
        `#discipline-${numberOfEducations}`,
        defaultDisciplineList
      );
      // Add input event listener to the new school select
      const newSchoolsList = document.querySelector(
        `.js-school-${numberOfEducations}`
      );
      newSchoolsList.addEventListener(
        "input",
        debounce(async (e) => {
          const datalistElement = document.querySelector(
            `#school-${numberOfEducations}`
          );
          var schools = [];
          if (newSchoolsList.value !== "") {
            schools = await getDataFromGreenhouseApi(
              "schools",
              newSchoolsList.value
            );
          }
          var list = "";
          schools.forEach((school) => {
            list += `<option value="${school.text}" />`;
          });
          datalistElement.innerHTML = list;
        }, 350)
      );
    });
  }

  if (locateMeButton) {
    locateMeButton.addEventListener("click", () => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (pos) => {
            fetch(
              `${url}${pos.coords.longitude},${pos.coords.latitude}.json?access_token=${API_KEY}&autocomplete=true&types=place%2Clocality`
            )
              .then((res) => {
                return res.json();
              })
              .then((response) => {
                locationLabel.value = response.features[0].place_name;
              })
              .catch((error) => console.error("Error:", error));
          },
          () => {
            locateMeError.classList.remove("u-hide");
            setTimeout(() => {
              locateMeError.classList.add("u-hide");
            }, 4000);
          }
        );
      } else {
        console.log("Geolocation is not supported by this browser.");
      }
    });
  }

  function debounce(func, wait, immediate) {
    var timeout;
    return function () {
      var context = this,
        args = arguments;
      clearTimeout(timeout);
      timeout = setTimeout(function () {
        timeout = null;
        if (!immediate) func.apply(context, args);
      }, wait);
      if (immediate && !timeout) func.apply(context, args);
    };
  }
})();

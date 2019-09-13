(function () {
  // Mapbox api 
  API_KEY = "pk.eyJ1IjoiY2Fub25pY2FsLXdlYnRlYW0iLCJhIjoiY2swZ3M0Y2tpMDNvMzNubGo1NG9pajZqMiJ9.v8qNlzrS4_gI5pJZQTAFaQ"
  url = "https://api.mapbox.com/geocoding/v5/mapbox.places/"

  addEducationButton = document.querySelector(".js-add-education");
  locateMeButton = document.querySelector(".js-locate-me");
  locateMeError = document.querySelector(".js-locate-error");
  locationLabel = document.querySelector(".js-location");

  addEducationButton.addEventListener("click", () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition);
    } else {
      locationLabel.text = "Geolocation is not supported by this browser.";
    }
    console.log(locationLabel);
  });

  locateMeButton.addEventListener("click", () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((pos) => {
        fetch(`${url}${pos.coords.longitude},${pos.coords.latitude}.json?access_token=${API_KEY}&autocomplete=true&types=place%2Clocality`)
          .then(res => { return res.json() })
          .then(response => {
            locationLabel.value = response.features[0].place_name
          })
          .catch(error => console.error('Error:', error));
      }, () => { 
        locateMeError.classList.remove("u-hide");
        setTimeout(() => {
          locateMeError.classList.add("u-hide");
        }, 4000)
      });
    } else {
      alert("Not available")
      // locationLabel.value = "Geolocation is not supported by this browser.";
    }
  });
})();
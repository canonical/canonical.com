function initMap() {
  const center = isSprintMap
    ? { lat: 38.44079856183539, lng: -32.13058355540764 }
    : { lat: 40.5074, lng: 30.1278 };
  const map = new google.maps.Map(document.getElementById("locations-map"), {
    zoom: 3,
    center,
  });

  const mapDiv = document.getElementById("locations-map");
  mapDiv.style.height = "25rem";

  // Change map center for smaller screens
  const screenWidth = window.screen.availWidth;
  if (screenWidth <= 1035 && screenWidth > 280) {
    map.setCenter({
      lat: 49.44547224793554,
      lng: 15.89044708488471,
    });
  } else if (screenWidth <= 280) {
    map.setCenter({
      lat: 46.875651470802104,
      lng: 7.99805750339787,
    });
  }

  // Create an info window to share between markers.
  const infoWindow = new google.maps.InfoWindow();

  // Create the markers.
  locations.forEach(([position, title], i) => {
    const marker = new google.maps.Marker({
      position,
      map,
      title: title,
      optimized: false,
    });

    // Add a click listener for each marker, and set up the info window.
    marker.addListener("click", () => {
      infoWindow.close();
      infoWindow.setContent(marker.getTitle());
      infoWindow.open(marker.getMap(), marker);
    });
  });
}

export { initMap };
window.initMap = initMap;

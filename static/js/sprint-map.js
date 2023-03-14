function initMap() {
  const map = new google.maps.Map(document.getElementById("sprint-map"), {
    zoom: 3,
    center: { lat: 38.44079856183539, lng: -32.13058355540764 },
  });
  
  const mapDiv = document.getElementById("sprint-map");
  mapDiv.style.height = "25rem";
  
  // Change map center for smaller screens
  const screenWidth = window.screen.availWidth;
  if ( screenWidth <= 620 ) {
    map.setCenter({
      lat : 49.44547224793554,
      lng : 15.89044708488471
    });
  }


  // Create an info window to share between markers.
  const infoWindow = new google.maps.InfoWindow();

  // Create the markers.
  sprintLocations.forEach(([position, title], i) => {
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

window.initMap = initMap;
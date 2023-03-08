function initMap() {
  const map = new google.maps.Map(document.getElementById("sprint-map"), {
    zoom: 3,
    center: { lat: 38.44079856183539, lng: -32.13058355540764 },
  });

  const sprintLocations = [
    [{ lat: 51.53910042435768, lng: -0.1416575585467801 }, "London"],
    [{ lat: -33.876169534561576, lng: 18.382182743342554 }, "Cape Town"],
    [{ lat: 55.67473557077814, lng: 12.602819433367 }, "Copenhagen"],
    [{ lat: 50.09169724226367, lng: 14.37895031427894 }, "Prague"],
    [{ lat: 50.142222694420674, lng: 8.614639914385569 }, "Frankfurt"],
    [{ lat: 45.50800862995117, lng: -73.58280686860392 }, "Montreal"],
    [{ lat: 40.798155988207235, lng: -73.85861239168297 }, "New York City"],
    [{ lat: 25.019212561496353, lng: 121.46383373680085 }, "Taipei"],
    [{ lat: 30.355265001335628, lng: -97.76687845245245 }, "Austin"],
    [{ lat: 48.857074990278676, lng: 2.3395547447652056 }, "Paris"],
    [{ lat: 29.767193226058257, lng: -95.3670538129764 }, "Houston"],
    [{ lat: -31.043359293503908, lng: 25.51255683173218 }, "Spier"],
    [{ lat: 35.8932740016975, lng: 14.43746658277917 }, "Malta"],
    [{ lat: 45.76429262112831, lng: 4.835301390987176 }, "Lyon"],
    [{ lat: 38.67917381627824, lng: -90.20103074315858 }, "St. Louis"],
    [{ lat: 49.345532689469906, lng: -123.15343044637059  }, "Vancouver"],
    [{ lat: 45.50646706624962, lng: -73.54839431247403 }, "Montreal"],
    [{ lat: 54.23314227514377, lng: -4.491204453385781 }, "Isle of Man"],
    [{ lat: 43.69252498079002, lng: -79.35691360946339 }, "Toronto"],
    [{ lat: 52.546559646531676, lng: 13.479878094105333 }, "Berlin"],
    [{ lat: 47.51053153079359, lng: 19.092692050422652 }, "Budapest"],
    [{ lat: 45.5599016546521, lng: -122.57976576863925 }, "Portland"],
    [{ lat: 39.9506480530072, lng: -75.15098887376676 }, "Philidelphia"],
    [{ lat: 37.63173475246442, lng: 127.01153111181107 }, "Seoul"],
    [{ lat: 50.93434695845433, lng: 4.383602900267246 }, "Brussels"],
    [{ lat: 49.25917985619196, lng: 16.627178100791575 }, "Brno"],
    [{ lat: -27.4687724806326, lng: 153.02599001382598 }, "Brisbane"],
    [{ lat: -33.865841276697054, lng: 151.196327385238 }, "Sydney"],
    [{ lat: 30.356430163416317, lng: -97.71716022646561 }, "Austin"],
    [{ lat: -33.45421283631078, lng: -70.66577622308252 }, "Santiago"],
    [{ lat: 39.748447785422016, lng: -105.0168199879092 }, "Denver"],
    [{ lat: 30.05563678743736, lng: -89.82322663188988 }, "New Orleans"],
    [{ lat: 52.24325667424824, lng: 21.05145033879068 }, "Warsaw"],
    [{ lat: 42.446882419194324, lng: -71.22491732631751 }, "Lexington"],
    [{ lat: 34.35676353830776, lng: -111.51505767860898 }, "Arizona"],
    [{ lat: 25.763155578558653, lng: 54.94246340504953 }, "Dubai"],
    [{ lat: 47.65006756574396, lng: -122.35867431899362 }, "Seattle"],
    [{ lat: 37.42579354504801, lng: -78.17007396261319 }, "Virginia"],
    [{ lat: 41.078424184612594, lng: -9.051132205419249 }, "Portugal"],
    [{ lat: 14.567870738893827, lng: 120.93577783953602 }, "Manilla"],
    [{ lat: 39.382464124962944, lng: -105.64887008422835 }, "Colorado"],
    [{ lat: 40.77912659323516, lng: -112.04853012171523 }, "Salt Lake City"],
    [{ lat: 52.57604547428001, lng: -0.1826908772221332 }, "Peterborough"],
    [{ lat: 37.9823636439218, lng: 23.7456050381961 }, "Athens"],
    [{ lat: 49.47243608230826, lng: 11.19116713398345 }, "Nuremberg"],
    [{ lat: 44.47558032183258, lng: 26.094270552088407 }, "Bucharest"],
    [{ lat: 51.051617091670444, lng: 3.732070061271262 }, "Ghent"],
    [{ lat: 25.761635180712478, lng: -80.20101769294185 }, "Miami"],
    [{ lat: 45.901473355934364, lng: 6.13502570130426 }, "Annecy"],
    [{ lat: 51.234949685621814, lng: 3.2142528855251635 }, "Bruges"],
    [{ lat: 28.535137392578626, lng: -81.4092377509802 }, "Orlando"],
  ];
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
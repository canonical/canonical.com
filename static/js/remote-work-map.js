import L from "leaflet";
// Natural Earth 1:110m countries GeoJSON, v5.1.2 (public domain).
// Source: https://github.com/nvkelso/natural-earth-vector/blob/v5.1.2/geojson/ne_110m_admin_0_countries.geojson
import countries from "./data/natural-earth-countries.json";

function initRemoteWorkMap() {
  const mapElement = document.getElementById("locations-map");

  if (!mapElement) {
    return;
  }

  const locations = JSON.parse(
    document.getElementById("sprint-locations").textContent
  );

  const map = L.map(mapElement, {
    minZoom: 2,
    maxZoom: 6,
    maxBounds: [
      [-75, -180],
      [80, 180],
    ],
    maxBoundsViscosity: 1.0,
  }).setView([31.505, -0.09], 2);

  L.geoJSON(countries, {
    attribution:
      '&copy; <a href="https://www.naturalearthdata.com/">Natural Earth</a>',
    interactive: false,
    style: {
      color: "#999",
      weight: 1,
      fillColor: "#fff",
      fillOpacity: 1,
    },
  }).addTo(map);

  const customIcon = L.icon({
    iconUrl: "https://assets.ubuntu.com/v1/dc208dc9-marker_updated_x1.png",
    iconRetinaUrl:
      "https://assets.ubuntu.com/v1/9235a64a-marker_updated_2x.png",
    iconSize: [20, 32.8],
    iconAnchor: [10, 32.8],
    popupAnchor: [0, -32.8],
  });

  locations.forEach(([position, city]) => {
    L.marker([position.lat, position.lng], { icon: customIcon })
      .bindPopup(city)
      .addTo(map);
  });
}

initRemoteWorkMap();

export { initRemoteWorkMap };

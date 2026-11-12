/**
 * Shared Leaflet map for location maps. Renders every `.js-map` element on
 * the page, each with its own view and optional markers:
 *
 * ```html
 * <div class="p-map js-map"
 *      data-map-center-lat="0"
 *      data-map-center-lng="0"
 *      data-map-zoom="2"
 *      data-map-points="example-points"
 *      role="region"
 *      aria-label="Map of example locations"></div>
 * <script id="example-points" type="application/json" nonce="{{ csp_nonce }}">
 *   [[{"lat": 51.5, "lng": -0.1}, "London"]]
 * </script>
 * <script src="{{ versioned_static('js/dist/locations-map.js') }}"
 *         nonce="{{ csp_nonce }}"></script>
 * ```
 *
 * - `data-map-center-lat`, `data-map-center-lng` and `data-map-zoom` set the
 *   default view (zoom levels 2–6, bounded to the world).
 * - `data-map-points` (optional) is the ID of a JSON script containing
 *   `[position, label]` pairs; labels are displayed as text.
 * - `data-map-responsive-views` (optional) is a JSON array of
 *   `{maxWidth, lat, lng, zoom?}` objects, ordered narrowest to widest; the
 *   first matching view overrides the default, including on resize.
 *
 * Include the bundled script once, after all maps and their JSON scripts.
 * Browser tests: `yarn playwright test --project=maps`.
 */
import L from "leaflet";
// Natural Earth 1:110m countries GeoJSON, v5.1.2 (public domain).
// Source: https://github.com/nvkelso/natural-earth-vector/blob/v5.1.2/geojson/ne_110m_admin_0_countries.geojson
import countries from "./data/natural-earth-countries.json";

/** Symbol used to store the Leaflet map instance on an element. */
const MAP_INSTANCE = Symbol("leafletMap");

/**
 * Returns the responsive view matching the current viewport, or undefined.
 * Responsive views must be ordered by ascending maxWidth.
 */
function getResponsiveView(responsiveViews) {
  return responsiveViews.find(({ maxWidth }) => window.innerWidth <= maxWidth);
}

/**
 * Computes the current view (center and zoom) based on data attributes and
 * responsive overrides.
 */
function getCurrentView(mapElement) {
  const { mapCenterLat, mapCenterLng, mapZoom, mapResponsiveViews } =
    mapElement.dataset;
  const responsiveViews = JSON.parse(mapResponsiveViews || "[]");
  const responsiveView = getResponsiveView(responsiveViews);

  return {
    center: [
      Number(responsiveView?.lat ?? mapCenterLat),
      Number(responsiveView?.lng ?? mapCenterLng),
    ],
    zoom: Number(responsiveView?.zoom ?? mapZoom),
    responsiveViews,
  };
}

/** Initializes a map element, unless it already has a map instance. */
function initMap(mapElement) {
  // Guard against re-initialization
  if (mapElement[MAP_INSTANCE]) return;

  const { mapPoints } = mapElement.dataset;
  const pointsScript = mapPoints && document.getElementById(mapPoints);
  if (mapPoints && !pointsScript) {
    console.warn(
      `Map points script "#${mapPoints}" not found; rendering map without markers.`
    );
  }
  const points = pointsScript ? JSON.parse(pointsScript.textContent) : [];
  const { center, zoom, responsiveViews } = getCurrentView(mapElement);

  if (!center.every(Number.isFinite) || !Number.isFinite(zoom)) {
    console.warn("Skipping map with invalid center or zoom.", mapElement);
    return;
  }

  const map = L.map(mapElement, {
    minZoom: 2,
    maxZoom: 6,
    maxBounds: [
      [-75, -180],
      [80, 180],
    ],
    maxBoundsViscosity: 1.0,
  }).setView(center, zoom);

  // Store instance to prevent re-initialization and enable resize updates
  mapElement[MAP_INSTANCE] = map;

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

  points.forEach(([position, label]) => {
    const popupContent = document.createElement("span");
    popupContent.textContent = label;

    L.marker([position.lat, position.lng], {
      icon: customIcon,
      title: label,
      alt: label,
    })
      .bindPopup(popupContent)
      .addTo(map);
  });

  // Update view when crossing responsive breakpoints
  if (responsiveViews.length > 0) {
    let lastView = getResponsiveView(responsiveViews);

    window.addEventListener("resize", () => {
      const currentView = getResponsiveView(responsiveViews);
      // Only update if we crossed into a different breakpoint
      if (currentView?.maxWidth !== lastView?.maxWidth) {
        lastView = currentView;
        const { center: newCenter, zoom: newZoom } = getCurrentView(mapElement);
        map.setView(newCenter, newZoom);
      }
    });
  }
}

function initMaps() {
  // Isolate failures so one misconfigured map doesn't break the others
  document.querySelectorAll(".js-map").forEach((mapElement) => {
    try {
      initMap(mapElement);
    } catch (error) {
      console.error("Failed to initialize map.", mapElement, error);
    }
  });
}

initMaps();

export { initMaps, MAP_INSTANCE };

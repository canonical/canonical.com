/** @jest-environment jsdom */

jest.mock("leaflet", () => ({
  map: jest.fn(() => {
    const map = { setView: jest.fn() };
    map.setView.mockReturnValue(map);
    return map;
  }),
  geoJSON: jest.fn(() => ({ addTo: jest.fn() })),
  icon: jest.fn(() => "map-icon"),
  marker: jest.fn(() => {
    const marker = { bindPopup: jest.fn(), addTo: jest.fn() };
    marker.bindPopup.mockReturnValue(marker);
    return marker;
  }),
}));

import L from "leaflet";
import countries from "../../static/js/data/natural-earth-countries.json";
import { initMaps, MAP_INSTANCE } from "../../static/js/locations-map.js";

describe("shared location maps", () => {
  const originalWidth = window.innerWidth;
  const resizeListeners = [];
  const firstView = { lat: 31.505, lng: -0.09, zoom: 2 };
  const secondView = { lat: 0, lng: 139.75, zoom: 4 };
  const firstPoints = [
    [{ lat: 51.5, lng: -0.1 }, "London"],
    [{ lat: 45.5, lng: -73.5 }, "Montreal"],
  ];
  const secondPoints = [
    [{ lat: 35.6, lng: 139.7 }, "<strong>Tokyo</strong>"],
  ];
  const smallView = { maxWidth: 280, lat: -20, lng: 10, zoom: 4 };
  const mediumView = { maxWidth: 1035, lat: 50, lng: 15 };

  beforeEach(() => {
    document.body.innerHTML = `
      <div id="first-map" class="js-map"
           data-map-center-lat="${firstView.lat}" data-map-center-lng="${firstView.lng}"
           data-map-zoom="${firstView.zoom}" data-map-points="first-points"></div>
      <div id="second-map" class="js-map"
           data-map-center-lat="${secondView.lat}" data-map-center-lng="${secondView.lng}"
           data-map-zoom="${secondView.zoom}" data-map-points="second-points"></div>
      <script id="first-points" type="application/json">
        ${JSON.stringify(firstPoints)}
      </script>
      <script id="second-points" type="application/json">
        ${JSON.stringify(secondPoints)}
      </script>
    `;
    jest.clearAllMocks();
    resizeListeners.length = 0;
    jest
      .spyOn(window, "addEventListener")
      .mockImplementation((event, handler) => {
        if (event === "resize") resizeListeners.push(handler);
      });
  });

  afterEach(() => {
    window.innerWidth = originalWidth;
    jest.restoreAllMocks();
  });

  it("initializes each map using its own numeric view attributes", () => {
    initMaps();

    expect(L.map).toHaveBeenCalledTimes(2);
    expect(L.map).toHaveBeenNthCalledWith(
      1,
      document.getElementById("first-map"),
      expect.objectContaining({ minZoom: 2, maxZoom: 6 })
    );
    expect(L.map).toHaveBeenNthCalledWith(
      2,
      document.getElementById("second-map"),
      expect.any(Object)
    );
    expect(L.map.mock.results[0].value.setView).toHaveBeenCalledWith(
      [firstView.lat, firstView.lng],
      firstView.zoom
    );
    expect(L.map.mock.results[1].value.setView).toHaveBeenCalledWith(
      [secondView.lat, secondView.lng],
      secondView.zoom
    );
  });

  it.each([
    [smallView.maxWidth, smallView, smallView.zoom],
    [smallView.maxWidth + 1, mediumView, firstView.zoom],
    [mediumView.maxWidth, mediumView, firstView.zoom],
    [mediumView.maxWidth + 1, firstView, firstView.zoom],
  ])("uses the configured starting view at %ipx", (width, view, zoom) => {
    window.innerWidth = width;
    document.getElementById("first-map").dataset.mapResponsiveViews =
      JSON.stringify([smallView, mediumView]);

    initMaps();

    expect(L.map.mock.results[0].value.setView).toHaveBeenCalledWith(
      [view.lat, view.lng],
      zoom
    );
    expect(L.map.mock.results[1].value.setView).toHaveBeenCalledWith(
      [secondView.lat, secondView.lng],
      secondView.zoom
    );
  });

  it("adds the shared geography and markers to the appropriate maps", () => {
    initMaps();

    const firstMap = L.map.mock.results[0].value;
    const secondMap = L.map.mock.results[1].value;
    expect(L.geoJSON).toHaveBeenCalledTimes(2);
    expect(L.geoJSON).toHaveBeenCalledWith(
      countries,
      expect.objectContaining({
        attribution: expect.stringContaining("Natural Earth"),
        interactive: false,
      })
    );
    expect(L.geoJSON.mock.results[0].value.addTo).toHaveBeenCalledWith(
      firstMap
    );
    expect(L.geoJSON.mock.results[1].value.addTo).toHaveBeenCalledWith(
      secondMap
    );

    expect(L.marker).toHaveBeenCalledTimes(3);
    [...firstPoints, ...secondPoints].forEach(([position, label], index) => {
      expect(L.marker).toHaveBeenNthCalledWith(
        index + 1,
        [position.lat, position.lng],
        {
          icon: "map-icon",
          title: label,
          alt: label,
        }
      );
    });
    expect(L.marker.mock.results[0].value.addTo).toHaveBeenCalledWith(firstMap);
    expect(L.marker.mock.results[1].value.addTo).toHaveBeenCalledWith(firstMap);
    expect(L.marker.mock.results[2].value.addTo).toHaveBeenCalledWith(
      secondMap
    );

    const popup = L.marker.mock.results[2].value.bindPopup.mock.calls[0][0];
    expect(popup.textContent).toBe(secondPoints[0][1]);
    expect(popup.querySelector("strong")).toBeNull();
  });

  it("anchors each pin at its bottom center", () => {
    initMaps();

    expect(L.icon).toHaveBeenCalledWith(
      expect.objectContaining({
        iconSize: [20, 32.8],
        iconAnchor: [10, 32.8],
        popupAnchor: [0, -32.8],
      })
    );
  });

  it("renders a map without a points script", () => {
    document.getElementById("first-map").removeAttribute("data-map-points");
    document.getElementById("second-map").remove();

    initMaps();

    expect(L.map).toHaveBeenCalledTimes(1);
    expect(L.geoJSON).toHaveBeenCalledTimes(1);
    expect(L.marker).not.toHaveBeenCalled();
  });

  it("renders a map without markers when its points script is missing", () => {
    const warn = jest.spyOn(console, "warn").mockImplementation(() => {});
    document.getElementById("first-points").remove();

    initMaps();

    expect(L.map).toHaveBeenCalledTimes(2);
    expect(L.marker).toHaveBeenCalledTimes(1);
    expect(L.marker.mock.results[0].value.addTo).toHaveBeenCalledWith(
      L.map.mock.results[1].value
    );
    expect(warn).toHaveBeenCalledWith(
      expect.stringContaining("#first-points")
    );
  });

  it("skips a map with an invalid view but initializes the others", () => {
    const warn = jest.spyOn(console, "warn").mockImplementation(() => {});
    document.getElementById("first-map").dataset.mapCenterLat = "not-a-number";

    initMaps();

    expect(L.map).toHaveBeenCalledTimes(1);
    expect(L.map).toHaveBeenCalledWith(
      document.getElementById("second-map"),
      expect.any(Object)
    );
    expect(warn).toHaveBeenCalledWith(
      expect.stringContaining("invalid center or zoom"),
      document.getElementById("first-map")
    );
  });

  it("continues initializing maps when one has malformed points JSON", () => {
    const error = jest.spyOn(console, "error").mockImplementation(() => {});
    document.getElementById("first-points").textContent = "{not json";

    initMaps();

    expect(L.map).toHaveBeenCalledTimes(1);
    expect(L.map).toHaveBeenCalledWith(
      document.getElementById("second-map"),
      expect.any(Object)
    );
    expect(error).toHaveBeenCalledWith(
      expect.stringContaining("Failed to initialize map."),
      document.getElementById("first-map"),
      expect.any(SyntaxError)
    );
  });

  it("does nothing when no map elements are present", () => {
    document.body.innerHTML = "";

    initMaps();

    expect(L.map).not.toHaveBeenCalled();
  });

  it("uses a trimmed Natural Earth feature collection", () => {
    expect(countries.type).toBe("FeatureCollection");
    expect(countries.features.length).toBeGreaterThan(0);
    expect(
      countries.features.every(
        (feature) =>
          Object.keys(feature.properties).length === 0 &&
          Object.keys(feature.geometry).sort().join(",") === "coordinates,type"
      )
    ).toBe(true);
  });

  it("skips re-initialization when initMaps is called twice", () => {
    initMaps();
    const firstMapElement = document.getElementById("first-map");
    const storedInstance = firstMapElement[MAP_INSTANCE];

    expect(L.map).toHaveBeenCalledTimes(2);
    expect(storedInstance).toBeDefined();

    initMaps();

    expect(L.map).toHaveBeenCalledTimes(2);
    expect(firstMapElement[MAP_INSTANCE]).toBe(storedInstance);
  });

  it("updates the view when resizing across a responsive breakpoint", () => {
    const smallResizeView = { ...smallView, maxWidth: 400 };
    const mediumResizeView = { ...mediumView, maxWidth: 800, zoom: 3 };
    window.innerWidth = 1200;
    document.getElementById("first-map").dataset.mapResponsiveViews =
      JSON.stringify([smallResizeView, mediumResizeView]);
    document.getElementById("second-map").remove();

    initMaps();

    const map = L.map.mock.results[0].value;
    expect(map.setView).toHaveBeenCalledTimes(1);
    expect(map.setView).toHaveBeenLastCalledWith(
      [firstView.lat, firstView.lng],
      firstView.zoom
    );

    // Resize within the same bracket (no breakpoint crossed)
    window.innerWidth = 1000;
    resizeListeners.forEach((handler) => handler());
    expect(map.setView).toHaveBeenCalledTimes(1);

    // Cross into the 800px breakpoint
    window.innerWidth = 700;
    resizeListeners.forEach((handler) => handler());
    expect(map.setView).toHaveBeenCalledTimes(2);
    expect(map.setView).toHaveBeenLastCalledWith(
      [mediumResizeView.lat, mediumResizeView.lng],
      mediumResizeView.zoom
    );

    // Stay in the same bracket
    window.innerWidth = 600;
    resizeListeners.forEach((handler) => handler());
    expect(map.setView).toHaveBeenCalledTimes(2);

    // Cross into the 400px breakpoint
    window.innerWidth = 350;
    resizeListeners.forEach((handler) => handler());
    expect(map.setView).toHaveBeenCalledTimes(3);
    expect(map.setView).toHaveBeenLastCalledWith(
      [smallResizeView.lat, smallResizeView.lng],
      smallResizeView.zoom
    );

    // Cross back out to 800px breakpoint
    window.innerWidth = 500;
    resizeListeners.forEach((handler) => handler());
    expect(map.setView).toHaveBeenCalledTimes(4);
    expect(map.setView).toHaveBeenLastCalledWith(
      [mediumResizeView.lat, mediumResizeView.lng],
      mediumResizeView.zoom
    );

    window.innerWidth = 1200;
    resizeListeners.forEach((handler) => handler());
    expect(map.setView).toHaveBeenCalledTimes(5);
    expect(map.setView).toHaveBeenLastCalledWith(
      [firstView.lat, firstView.lng],
      firstView.zoom
    );
  });

  it("does not register a resize listener without responsive views", () => {
    document.getElementById("second-map").remove();

    initMaps();

    expect(resizeListeners).toHaveLength(0);
  });
});

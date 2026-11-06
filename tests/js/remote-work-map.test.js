/** @jest-environment jsdom */

jest.mock("leaflet", () => ({
  map: jest.fn(() => {
    const map = { setView: jest.fn() };
    map.setView.mockReturnValue(map);
    return map;
  }),
  geoJSON: jest.fn(() => ({ addTo: jest.fn() })),
  icon: jest.fn(() => "map-icon"),
  marker: jest.fn(() => ({
    bindPopup: jest.fn(() => ({ addTo: jest.fn() })),
  })),
}));

import L from "leaflet";
import countries from "../../static/js/data/natural-earth-countries.json";
import { initRemoteWorkMap } from "../../static/js/remote-work-map.js";

describe("remote-work-map", () => {
  beforeEach(() => {
    document.body.innerHTML = '<div id="locations-map"></div>';
    const locations = document.createElement("script");
    locations.id = "sprint-locations";
    locations.type = "application/json";
    locations.textContent = JSON.stringify([
      [{ lat: 45.50800862995117, lng: -73.58280686860392 }, "Montreal"],
      [{ lat: 21.1619, lng: -86.8515 }, "Cancun"],
    ]);
    document.body.appendChild(locations);
    jest.clearAllMocks();
  });

  it("renders Natural Earth geometry and location markers", () => {
    initRemoteWorkMap();

    expect(L.geoJSON).toHaveBeenCalledWith(
      countries,
      expect.objectContaining({
        attribution: expect.stringContaining("Natural Earth"),
        interactive: false,
      })
    );
    expect(L.marker).toHaveBeenCalledTimes(2);
    expect(L.marker).toHaveBeenCalledWith(
      [45.50800862995117, -73.58280686860392],
      {
        icon: "map-icon",
      }
    );
    expect(L.marker).toHaveBeenCalledWith([21.1619, -86.8515], {
      icon: "map-icon",
    });
    expect(L.marker.mock.results[1].value.bindPopup).toHaveBeenCalledWith(
      "Cancun"
    );
  });

  it("does not create a map when the map element is absent", () => {
    document.body.innerHTML = "";

    initRemoteWorkMap();

    expect(L.map).not.toHaveBeenCalled();
  });

  it("anchors each pin at its bottom center", () => {
    initRemoteWorkMap();

    expect(L.icon).toHaveBeenCalledWith(
      expect.objectContaining({
        iconSize: [20, 32.8],
        iconAnchor: [10, 32.8],
        popupAnchor: [0, -32.8],
      })
    );
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
});

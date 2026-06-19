/** @jest-environment jsdom */

import { initMap } from "../../static/js/locations-map.js";

describe("locations-map", () => {
  let mockMap;
  let mockMarker;
  let mockInfoWindow;
  let mockMapDiv;

  beforeEach(() => {
    // Setup DOM
    document.body.innerHTML = '<div id="locations-map"></div>';
    mockMapDiv = document.getElementById("locations-map");

    // Mock Google Maps
    mockInfoWindow = {
      close: jest.fn(),
      setContent: jest.fn(),
      open: jest.fn(),
    };

    mockMarker = {
      addListener: jest.fn(),
      getMap: jest.fn(() => mockMap),
      getTitle: jest.fn(() => "Test Location"),
    };

    mockMap = {
      setCenter: jest.fn(),
    };

    global.google = {
      maps: {
        Map: jest.fn(() => mockMap),
        Marker: jest.fn(() => mockMarker),
        InfoWindow: jest.fn(() => mockInfoWindow),
      },
    };

    // Setup global variables
    global.isSprintMap = false;
    global.locations = [
      [{ lat: 40.7128, lng: -74.006 }, "New York"],
      [{ lat: 34.0522, lng: -118.2437 }, "Los Angeles"],
      [{ lat: 41.8781, lng: -87.6298 }, "Chicago"],
    ];

    // Mock screen
    Object.defineProperty(window, "screen", {
      value: { availWidth: 1920 },
      writable: true,
      configurable: true,
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe("Map initialization", () => {
    it("should create a map with default center for regular map", () => {
      initMap();

      expect(global.google.maps.Map).toHaveBeenCalledWith(mockMapDiv, {
        zoom: 3,
        center: { lat: 40.5074, lng: 30.1278 },
      });
    });

    it("should create a map with sprint map center when isSprintMap is true", () => {
      global.isSprintMap = true;
      initMap();

      expect(global.google.maps.Map).toHaveBeenCalledWith(mockMapDiv, {
        zoom: 3,
        center: { lat: 38.44079856183539, lng: -32.13058355540764 },
      });
    });

    it("should set map div height to 25rem", () => {
      initMap();

      expect(mockMapDiv.style.height).toBe("25rem");
    });

    it("should create an InfoWindow", () => {
      initMap();

      expect(global.google.maps.InfoWindow).toHaveBeenCalled();
    });
  });

  describe("Responsive center adjustment", () => {
    it("should adjust center for medium screens (537px to 1035px)", () => {
      Object.defineProperty(window, "screen", {
        value: { availWidth: 800 },
        writable: true,
        configurable: true,
      });

      initMap();

      expect(mockMap.setCenter).toHaveBeenCalledWith({
        lat: 49.44547224793554,
        lng: 15.89044708488471,
      });
    });

    it("should adjust center for small screens (281px to 536px)", () => {
      Object.defineProperty(window, "screen", {
        value: { availWidth: 400 },
        writable: true,
        configurable: true,
      });

      initMap();

      expect(mockMap.setCenter).toHaveBeenCalledWith({
        lat: 49.44547224793554,
        lng: 15.89044708488471,
      });
    });

    it("should adjust center for very small screens (<=280px)", () => {
      Object.defineProperty(window, "screen", {
        value: { availWidth: 280 },
        writable: true,
        configurable: true,
      });

      initMap();

      expect(mockMap.setCenter).toHaveBeenCalledWith({
        lat: 46.875651470802104,
        lng: 7.99805750339787,
      });
    });

    it("should not adjust center for large screens (>1035px)", () => {
      Object.defineProperty(window, "screen", {
        value: { availWidth: 1920 },
        writable: true,
        configurable: true,
      });

      initMap();

      expect(mockMap.setCenter).not.toHaveBeenCalled();
    });

    it("should not adjust at 281px (goes to medium)", () => {
      Object.defineProperty(window, "screen", {
        value: { availWidth: 281 },
        writable: true,
        configurable: true,
      });

      initMap();

      expect(mockMap.setCenter).toHaveBeenCalledWith({
        lat: 49.44547224793554,
        lng: 15.89044708488471,
      });
    });
  });

  describe("Marker creation", () => {
    it("should create a marker for each location", () => {
      initMap();

      expect(global.google.maps.Marker).toHaveBeenCalledTimes(3);
    });

    it("should create marker with correct position and title", () => {
      initMap();

      expect(global.google.maps.Marker).toHaveBeenNthCalledWith(1, {
        position: { lat: 40.7128, lng: -74.006 },
        map: mockMap,
        title: "New York",
        optimized: false,
      });

      expect(global.google.maps.Marker).toHaveBeenNthCalledWith(2, {
        position: { lat: 34.0522, lng: -118.2437 },
        map: mockMap,
        title: "Los Angeles",
        optimized: false,
      });

      expect(global.google.maps.Marker).toHaveBeenNthCalledWith(3, {
        position: { lat: 41.8781, lng: -87.6298 },
        map: mockMap,
        title: "Chicago",
        optimized: false,
      });
    });

    it("should set optimized to false", () => {
      initMap();

      global.google.maps.Marker.mock.calls.forEach((call) => {
        expect(call[0].optimized).toBe(false);
      });
    });

    it("should pass map instance to markers", () => {
      initMap();

      global.google.maps.Marker.mock.calls.forEach((call) => {
        expect(call[0].map).toBe(mockMap);
      });
    });

    it("should handle empty locations array", () => {
      global.locations = [];
      initMap();

      expect(global.google.maps.Marker).not.toHaveBeenCalled();
    });

    it("should handle single location", () => {
      global.locations = [[{ lat: 51.5074, lng: -0.1278 }, "London"]];
      initMap();

      expect(global.google.maps.Marker).toHaveBeenCalledTimes(1);
    });
  });

  describe("Marker click behavior", () => {
    it("should add click listener to each marker", () => {
      initMap();

      expect(mockMarker.addListener).toHaveBeenCalledTimes(3);
      expect(mockMarker.addListener).toHaveBeenCalledWith("click", expect.any(Function));
    });

    it("should close info window on marker click", () => {
      initMap();

      const clickHandler = mockMarker.addListener.mock.calls[0][1];
      clickHandler();

      expect(mockInfoWindow.close).toHaveBeenCalled();
    });

    it("should set info window content to marker title", () => {
      initMap();

      const clickHandler = mockMarker.addListener.mock.calls[0][1];
      clickHandler();

      expect(mockInfoWindow.setContent).toHaveBeenCalledWith("Test Location");
    });

    it("should open info window at correct location", () => {
      initMap();

      const clickHandler = mockMarker.addListener.mock.calls[0][1];
      clickHandler();

      expect(mockInfoWindow.open).toHaveBeenCalledWith(mockMap, mockMarker);
    });

    it("should execute click handler in correct order", () => {
      const callOrder = [];
      mockInfoWindow.close.mockImplementation(() => callOrder.push("close"));
      mockInfoWindow.setContent.mockImplementation(() => callOrder.push("setContent"));
      mockInfoWindow.open.mockImplementation(() => callOrder.push("open"));

      initMap();

      const clickHandler = mockMarker.addListener.mock.calls[0][1];
      clickHandler();

      expect(callOrder).toEqual(["close", "setContent", "open"]);
    });

    it("should share same info window across all markers", () => {
      initMap();

      global.google.maps.Marker.mock.calls.forEach((call) => {
        expect(call[0].map).toBe(mockMap);
      });

      // All markers should use same infoWindow from the closure
      expect(global.google.maps.InfoWindow).toHaveBeenCalledTimes(1);
    });

    it("should handle multiple marker clicks", () => {
      initMap();

      // Simulate clicking first marker
      let clickHandler = mockMarker.addListener.mock.calls[0][1];
      clickHandler();

      expect(mockInfoWindow.close).toHaveBeenCalledTimes(1);
      expect(mockInfoWindow.setContent).toHaveBeenCalledTimes(1);
      expect(mockInfoWindow.open).toHaveBeenCalledTimes(1);

      // Simulate clicking second marker
      clickHandler = mockMarker.addListener.mock.calls[1][1];
      clickHandler();

      expect(mockInfoWindow.close).toHaveBeenCalledTimes(2);
      expect(mockInfoWindow.setContent).toHaveBeenCalledTimes(2);
      expect(mockInfoWindow.open).toHaveBeenCalledTimes(2);
    });
  });

  describe("Integration scenarios", () => {
    it("should initialize sprint map with responsive settings", () => {
      global.isSprintMap = true;
      Object.defineProperty(window, "screen", {
        value: { availWidth: 600 },
        writable: true,
        configurable: true,
      });

      initMap();

      expect(global.google.maps.Map).toHaveBeenCalledWith(
        mockMapDiv,
        expect.objectContaining({
          center: { lat: 38.44079856183539, lng: -32.13058355540764 },
        })
      );

      expect(mockMap.setCenter).toHaveBeenCalledWith({
        lat: 49.44547224793554,
        lng: 15.89044708488471,
      });
    });

    it("should create fully functional map", () => {
      initMap();

      // Map created
      expect(global.google.maps.Map).toHaveBeenCalled();

      // Markers created
      expect(global.google.maps.Marker).toHaveBeenCalledTimes(3);

      // Info window created
      expect(global.google.maps.InfoWindow).toHaveBeenCalled();

      // Click listeners added
      expect(mockMarker.addListener).toHaveBeenCalledTimes(3);

      // Test a click
      const clickHandler = mockMarker.addListener.mock.calls[0][1];
      clickHandler();

      expect(mockInfoWindow.close).toHaveBeenCalled();
      expect(mockInfoWindow.setContent).toHaveBeenCalled();
      expect(mockInfoWindow.open).toHaveBeenCalled();
    });

    it("should handle map with multiple locations and small screen", () => {
      global.locations = [
        [{ lat: 52.52, lng: 13.405 }, "Berlin"],
        [{ lat: 48.8566, lng: 2.3522 }, "Paris"],
        [{ lat: 51.5074, lng: -0.1278 }, "London"],
        [{ lat: 40.7128, lng: -74.006 }, "New York"],
      ];

      Object.defineProperty(window, "screen", {
        value: { availWidth: 250 },
        writable: true,
        configurable: true,
      });

      initMap();

      expect(global.google.maps.Marker).toHaveBeenCalledTimes(4);
      expect(mockMap.setCenter).toHaveBeenCalledWith({
        lat: 46.875651470802104,
        lng: 7.99805750339787,
      });
    });
  });
});

import { expect, test, type Locator, type Page } from "@playwright/test";
import * as path from "path";
import { acceptCookiePolicy } from "../../helpers/commands";

type MapPoint = [{ lat: number; lng: number }, string];

const pages = [
  {
    path: "/company",
    marker: "London",
    locations: [
      "London",
      "USA",
      "Shanghai",
      "Beijing",
      "Taipei",
      "Isle of Man",
      "Tokyo",
    ],
  },
  {
    path: "/careers/company-culture/remote-work",
    marker: "Cape Town",
    locations: [
      "London",
      "Cape Town",
      "Copenhagen",
      "Prague",
      "Frankfurt",
      "Montreal",
      "Toronto",
      "Lyon",
      "Riga",
      "The Hague",
      "Madrid",
      "Vancouver",
      "Cancun",
    ],
  },
];

const pinUrl = "https://assets.ubuntu.com/v1/dc208dc9-marker_updated_x1.png";
const retinaPinUrl =
  "https://assets.ubuntu.com/v1/9235a64a-marker_updated_2x.png";

async function blockExternalRequests(page: Page) {
  await page.route("**/*", (route) => {
    const url = route.request().url();
    // Only known pin URLs receive local PNG fixtures; unexpected URLs stay blocked.
    if (url === pinUrl || url === retinaPinUrl) {
      return route.fulfill({
        contentType: "image/png",
        path: path.join(
          __dirname,
          "../../../../node_modules/leaflet/dist/images",
          url === pinUrl ? "marker-icon.png" : "marker-icon-2x.png"
        ),
      });
    }
    const { hostname } = new URL(url);
    return ["localhost", "127.0.0.1", "0.0.0.0"].includes(hostname)
      ? route.continue()
      : route.abort();
  });
}

async function expectDecodedPins(markers: Locator, url: string) {
  await expect
    .poll(() =>
      markers.evaluateAll(
        (images, expectedUrl) =>
          images.length > 0 &&
          images.every(
            (image) =>
              image instanceof HTMLImageElement &&
              image.currentSrc === expectedUrl &&
              image.complete &&
              image.naturalWidth > 0
          ),
        url
      )
    )
    .toBe(true);
}

async function pinOffset(marker: Locator) {
  return marker.evaluate((element) => {
    const map = element.closest(".js-map");
    if (!map) throw new Error("Pin is not inside a map");
    const mapRect = map.getBoundingClientRect();
    const pinRect = element.getBoundingClientRect();
    return {
      x: pinRect.x + pinRect.width / 2 - (mapRect.x + mapRect.width / 2),
      y: pinRect.bottom - (mapRect.y + mapRect.height / 2),
    };
  });
}

test.describe("location maps", () => {
  for (const { path, marker: label, locations } of pages) {
    for (const width of [1280, 375, 280]) {
      test(`${path} keeps its map and sample pin in bounds at ${width}px`, async ({
        page,
      }) => {
        await page.setViewportSize({ width, height: 900 });
        await blockExternalRequests(page);
        const response = await page.goto(path, { waitUntil: "load" });
        expect(response?.status()).toBe(200);
        await acceptCookiePolicy(page);

        const map = page.locator(".js-map");
        await expect(map).toHaveClass(/leaflet-container/);
        await expect(map).toHaveCSS("height", "400px");
        const marker = map.locator(`.leaflet-marker-icon[alt="${label}"]`);
        const mapBounds = await map.boundingBox();
        const markerBounds = await marker.boundingBox();
        expect(mapBounds).not.toBeNull();
        expect(markerBounds).not.toBeNull();
        if (!mapBounds || !markerBounds)
          throw new Error("Map or marker missing");
        expect(markerBounds.x).toBeGreaterThanOrEqual(mapBounds.x);
        expect(markerBounds.y).toBeGreaterThanOrEqual(mapBounds.y);
        expect(markerBounds.x + markerBounds.width).toBeLessThanOrEqual(
          mapBounds.x + mapBounds.width
        );
        expect(markerBounds.y + markerBounds.height).toBeLessThanOrEqual(
          mapBounds.y + mapBounds.height
        );
      });
    }

    test(`${path} renders every location with decoded pins and working controls`, async ({
      page,
    }) => {
      await page.setViewportSize({ width: 1280, height: 900 });
      await blockExternalRequests(page);
      await page.goto(path, { waitUntil: "load" });
      await acceptCookiePolicy(page);

      const map = page.locator(".js-map");
      await expect(
        map.locator(".leaflet-overlay-pane svg path").first()
      ).toBeAttached();
      await expect(map.locator(".leaflet-control-attribution")).toContainText(
        "Natural Earth"
      );

      const pointsId = await map.getAttribute("data-map-points");
      const pointsScript = page.locator(`script[id="${pointsId}"]`);
      await expect(pointsScript).toHaveAttribute("type", "application/json");
      const points: MapPoint[] = JSON.parse(await pointsScript.innerText());
      expect(points.map(([, location]) => location)).toEqual(locations);

      const markers = map.locator(".leaflet-marker-icon");
      await expect
        .poll(() =>
          markers.evaluateAll((images) =>
            images.map((image) => image.getAttribute("alt"))
          )
        )
        .toEqual(locations);
      await expectDecodedPins(markers, pinUrl);

      const marker = map.locator(`.leaflet-marker-icon[alt="${label}"]`);
      await map.evaluate((element) =>
        window.scrollBy(0, element.getBoundingClientRect().top - 220)
      );
      await marker.click();
      await expect(map.locator(".leaflet-popup-content")).toHaveText(label);

      const previousPosition = await marker.evaluate(
        (element) => element.style.transform
      );
      await map.locator(".leaflet-control-zoom-in").click();
      await expect
        .poll(() => marker.evaluate((element) => element.style.transform))
        .not.toBe(previousPosition);
    });
  }
});

test.describe("multiple maps on a high-density display", () => {
  test.use({ deviceScaleFactor: 2 });

  test("multiple maps use independent views and point lists", async ({
    page,
  }) => {
    const mapWidth = 600;
    const firstView = { lat: 0, lng: 0, zoom: 2 };
    const secondView = { lat: 0, lng: 45, zoom: 2 };
    const firstPoints: MapPoint[] = [
      [{ lat: firstView.lat, lng: firstView.lng }, "First"],
    ];
    const secondPoints: MapPoint[] = [
      [{ lat: firstView.lat, lng: firstView.lng }, "Second"],
      [{ lat: 10, lng: secondView.lng }, "Another"],
    ];
    const firstLabel = firstPoints[0][1];
    const secondLabel = secondPoints[0][1];
    await blockExternalRequests(page);
    await page.route("**/__map-fixture__", (route) =>
      route.fulfill({
        contentType: "text/html",
        body: `<!doctype html>
        <link rel="stylesheet" href="/static/css/styles.css">
        <div id="first-map" class="p-map js-map" style="width: ${mapWidth}px"
             data-map-center-lat="${firstView.lat}" data-map-center-lng="${
          firstView.lng
        }"
             data-map-zoom="${
               firstView.zoom
             }" data-map-points="first-points"></div>
        <div id="second-map" class="p-map js-map" style="width: ${mapWidth}px"
             data-map-center-lat="${secondView.lat}" data-map-center-lng="${
          secondView.lng
        }"
             data-map-zoom="${
               secondView.zoom
             }" data-map-points="second-points"></div>
        <div id="empty-map" class="p-map js-map" style="width: ${mapWidth}px"
             data-map-center-lat="${firstView.lat}" data-map-center-lng="${
          firstView.lng
        }"
             data-map-zoom="${firstView.zoom}"></div>
        <script id="first-points" type="application/json">
          ${JSON.stringify(firstPoints)}
        </script>
        <script id="second-points" type="application/json">
          ${JSON.stringify(secondPoints)}
        </script>
        <script src="/static/js/dist/locations-map.js"></script>`,
      })
    );
    await page.goto("/__map-fixture__");

    const first = page.locator("#first-map");
    const second = page.locator("#second-map");
    const empty = page.locator("#empty-map");
    await expect(first.locator(".leaflet-marker-icon")).toHaveCount(
      firstPoints.length
    );
    await expect(second.locator(".leaflet-marker-icon")).toHaveCount(
      secondPoints.length
    );
    await expectDecodedPins(page.locator(".leaflet-marker-icon"), retinaPinUrl);
    await expect(empty).toHaveClass(/leaflet-container/);
    await expect(empty.locator(".leaflet-marker-icon")).toHaveCount(0);

    const firstOffset = await first
      .locator(`[alt="${firstLabel}"]`)
      .evaluate((marker) => {
        const map = marker.closest(".js-map")!.getBoundingClientRect();
        const pin = marker.getBoundingClientRect();
        return pin.x + pin.width / 2 - map.x;
      });
    const secondOffset = await second
      .locator(`[alt="${secondLabel}"]`)
      .evaluate((marker) => {
        const map = marker.closest(".js-map")!.getBoundingClientRect();
        const pin = marker.getBoundingClientRect();
        return pin.x + pin.width / 2 - map.x;
      });
    expect(firstOffset).toBeCloseTo(mapWidth / 2, 0);
    const expectedSecondOffset =
      mapWidth / 2 +
      (256 * 2 ** secondView.zoom * (secondPoints[0][0].lng - secondView.lng)) /
        360;
    expect(secondOffset).toBeCloseTo(expectedSecondOffset, 0);

    await first.locator(`[alt="${firstLabel}"]`).click();
    await second.locator(`[alt="${secondLabel}"]`).click();
    await expect(first.locator(".leaflet-popup-content")).toHaveText(
      firstLabel
    );
    await expect(second.locator(".leaflet-popup-content")).toHaveText(
      secondLabel
    );
  });
});

test("map updates view when resizing across a responsive breakpoint", async ({
  page,
}) => {
  const wideViewport = { width: 1200, height: 900 };
  const defaultView = { lat: 0, lng: 0, zoom: 2 };
  const responsiveView = { maxWidth: 600, lat: 40, lng: 80, zoom: 3 };
  const defaultPoint: MapPoint = [
    { lat: defaultView.lat, lng: defaultView.lng },
    "Default",
  ];
  const targetPoint: MapPoint = [
    { lat: responsiveView.lat, lng: responsiveView.lng },
    "Target",
  ];
  const nearbyPoint: MapPoint = [
    { lat: responsiveView.lat, lng: responsiveView.lng + 10 },
    "Nearby",
  ];
  const points = [defaultPoint, targetPoint, nearbyPoint];
  await page.setViewportSize(wideViewport);
  await blockExternalRequests(page);
  await page.route("**/__resize-fixture__", (route) =>
    route.fulfill({
      contentType: "text/html",
      body: `<!doctype html>
        <link rel="stylesheet" href="/static/css/styles.css">
        <div id="responsive-map" class="p-map js-map" style="width: 100%"
             data-map-center-lat="${defaultView.lat}" data-map-center-lng="${
        defaultView.lng
      }"
             data-map-zoom="${defaultView.zoom}" data-map-points="points"
             data-map-responsive-views='${JSON.stringify([
               responsiveView,
             ])}'></div>
        <script id="points" type="application/json">
          ${JSON.stringify(points)}
        </script>
        <script src="/static/js/dist/locations-map.js"></script>`,
    })
  );
  await page.goto("/__resize-fixture__");

  const map = page.locator("#responsive-map");
  const marker = map.locator(`[alt="${targetPoint[1]}"]`);
  const defaultMarker = map.locator(`[alt="${defaultPoint[1]}"]`);
  const nearbyMarker = map.locator(`[alt="${nearbyPoint[1]}"]`);
  await expect(map).toHaveClass(/leaflet-container/);

  await expect
    .poll(async () => {
      const { x, y } = await pinOffset(defaultMarker);
      return Math.max(Math.abs(x), Math.abs(y));
    })
    .toBeLessThanOrEqual(1);
  const wideOffset = await pinOffset(marker);
  const expectedWideOffset = Math.round(
    (256 * 2 ** defaultView.zoom * (targetPoint[0].lng - defaultView.lng)) / 360
  );
  expect(wideOffset.x).toBeCloseTo(expectedWideOffset, 0);

  await page.setViewportSize({
    ...wideViewport,
    width: responsiveView.maxWidth,
  });
  await expect
    .poll(async () => {
      const { x, y } = await pinOffset(marker);
      return Math.max(Math.abs(x), Math.abs(y));
    })
    .toBeLessThanOrEqual(1);
  const expectedPinDistance = Math.round(
    (256 *
      2 ** responsiveView.zoom *
      (nearbyPoint[0].lng - targetPoint[0].lng)) /
      360
  );
  await expect
    .poll(async () => {
      const target = await pinOffset(marker);
      const nearby = await pinOffset(nearbyMarker);
      return nearby.x - target.x;
    })
    .toBeCloseTo(expectedPinDistance, 0);

  await page.setViewportSize(wideViewport);
  await expect
    .poll(async () => {
      const { x, y } = await pinOffset(defaultMarker);
      return Math.max(Math.abs(x), Math.abs(y));
    })
    .toBeLessThanOrEqual(1);
  await expect
    .poll(async () => {
      const restored = await pinOffset(marker);
      return Math.max(
        Math.abs(restored.x - wideOffset.x),
        Math.abs(restored.y - wideOffset.y)
      );
    })
    .toBeLessThanOrEqual(1);
});

test.describe("location maps without JavaScript", () => {
  test.use({ javaScriptEnabled: false });

  for (const { path, locations } of pages) {
    test(`${path} displays its location list`, async ({ page }) => {
      await blockExternalRequests(page);
      await page.goto(path, { waitUntil: "domcontentloaded" });
      const items = page.locator(".p-map li");
      await expect(items).toHaveText(locations);
      for (const item of await items.all()) {
        await expect(item).toBeVisible();
      }
    });
  }
});

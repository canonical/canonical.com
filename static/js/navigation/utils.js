import { navigation, topLevelNavigationItems } from "./elements";

function ensureDataLayerInitialized() {
  if (!window.dataLayer) {
    window.dataLayer = [];
  }
}

function getText(el) {
  if (!el) return "";
  return (el.textContent || "").trim();
}

// Derive a readable title for links or link-like elements
function getElementTitle(element) {
  if (!element) return "";

  const span = element.querySelector("span");
  if (span) return getText(span);

  // Prefer direct text nodes to avoid nested descriptions
  const directText = Array.from(element.childNodes)
    .filter((node) => node.nodeType === Node.TEXT_NODE)
    .map((node) => (node.textContent || "").trim())
    .join(" ")
    .trim();
  if (directText) return directText;

  // Fallback: remove known non-title elements and read remaining text
  const clone = element.cloneNode(true);
  clone.querySelectorAll("small, br").forEach((el) => el.remove());
  return (clone.textContent || "").trim();
}

function formatSegment(index, label) {
  const safeLabel = (label || "").toLowerCase();
  return `${index}. ${safeLabel}`;
}

function joinSegments(segments) {
  return segments.filter(Boolean).join(" | ");
}

function pushToDataLayer(values) {
  ensureDataLayerInitialized();
  window.dataLayer.push(values);
}

export {
  ensureDataLayerInitialized,
  getText,
  getElementTitle,
  formatSegment,
  joinSegments,
  pushToDataLayer
}
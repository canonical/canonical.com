const fs = require("fs");
const yaml = require("js-yaml");

// Snapshot configuration for Percy visual testing
const baseURL = "http://localhost:8002";
const timeout = 30000;

const acceptCookies = () => {
  const banner = document.querySelector(".cookie-policy");
  banner?.querySelector("#cookie-policy-button-accept-all")?.click();
};

// Common snapshot config factory
const makeSnapshot = ({ path, name }) => ({
  name,
  url: `${baseURL}${path === "/" ? "" : path}`,
  waitForTimeout: timeout,
  execute: { beforeSnapshot: acceptCookies },
});

const data = yaml.load(fs.readFileSync("test-links.yaml", "utf8"));

const routes = data.links.map((link) => ({
  path: link.url.replace("https://canonical.com/", "/"),
  name: link.name,
}));

module.exports = routes.map(makeSnapshot);
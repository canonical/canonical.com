import { navigation } from "../elements";

/**
 * Populate available roles for careers roles.
 * @param {Array} departments - Array of objects containing department slug and count of roles
 */
function updateHtmlWithRoles(departments) {
  departments.forEach((dpt) => {
    const departmentElements = navigation.querySelectorAll(
      `[data-id="${dpt.slug}"]`
    );
    departmentElements.forEach((element) => {
      element.innerHTML = `${dpt.count} roles`;
      element.classList.add("u-animation--slide-from-top");
    });
  });
}

/**
 * Primary: Fetch careers roles data uses a web worker and then populate the fields
 */
function fecthAvailableRolesWithWebWorkers() {
  const worker = new Worker(
    "/static/js/navigation/careers/Worker_populate-careers.js"
  );
  // trigger the web worker by calling it with an empty string
  worker.postMessage("");
  // once it has the data back populate the fields
  worker.onmessage = function (e) {
    updateHtmlWithRoles(e.data);
  };
}

/**
 * Fallback: Fetch careers roles data and then populate the fields
 */
function fecthAvailableRoles() {
  // fallback for older browsers that dont have access to web workers
  fetch("/careers/roles.json")
    .then((response) => response.json())
    .then((departments) => {
      updateHtmlWithRoles(departments);
    })
    .catch((error) => {
      console.error(`Unable to load careers navigation roles: ${error}`);
    });
}

export default function populateCareersRoles() {
  if (window.Worker) {
    fecthAvailableRolesWithWebWorkers();
  } else {
    fecthAvailableRoles();
  }
}

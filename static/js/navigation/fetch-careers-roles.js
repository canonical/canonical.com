/**
 * Function that is consumed by a webworker to fetch careers roles data
 * @param {Event} e
 */
self.onmessage = function (e) {
  fetch("/careers/roles.json")
    .then((response) => response.json())
    .then((departments) => {
      const processedData = departments.map((dpt) => ({
        slug: dpt.slug,
        count: dpt.count,
      }));
      self.postMessage(processedData);
    })
    .catch((error) => {
      console.error(`Unable to load careers navigation roles: ${error}`);
    });
};

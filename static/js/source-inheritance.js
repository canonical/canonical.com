function setSourceField() {
  if (sessionStorage.getItem("gh_src")) {
    const ghsrcField = document.getElementById("ghsrc");
    const ghsrc = sessionStorage.getItem("gh_src");
    if (ghsrc && ghsrcField) {
      ghsrcField.value = ghsrc;
    }
  }
}

function setSessionStorage() {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const ghsrc = urlParams.get("gh_src");

  if (ghsrc) {
    sessionStorage.setItem("gh_src", ghsrc);
  }
}

setSessionStorage();
setSourceField();

const form = document.getElementById("request-assessment-form");
const input = form.querySelector("#request-assessment-email");
const inputContainer = input.parentNode;
const errorMessage = form.querySelector("#exampleInputErrorMessage");
const buttons = form.querySelectorAll("footer button");
const loadingIcon = form.querySelector(".p-icon--spinner");
const submitButton = form.querySelector("#request-assessment-submit");
const closeModalButton = form.querySelector(".p-modal__close");
const requestBUttonContainer = document.getElementById(
  "reportRequestContainer"
);

submitButton.addEventListener("click", (e) => {
  e.preventDefault();
  runGet();
  fetch(form.dataset.action, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ "request-assessment-email": input.value }),
  })
    .then((response) => response.json())
    .then((response) => {
      finishGet(response);
    });
});

function runGet() {
  buttons.forEach((button) => {
    inputContainer.classList.remove("is-error");
    errorMessage.innerText = "";
    loadingIcon.classList.remove("u-hide");
    button.disabled = true;
  });
}

function finishGet(response) {
  if (response.status === "success") {
    const attachments = response.message;
    requestBUttonContainer.innerHTML = "";
    attachments.forEach((attachment) => {
      const downloadLink = document.createElement("a");
      downloadLink.innerHTML = `Download your candidate report`;
      downloadLink.download = true;
      downloadLink.href = attachment.url;
      downloadLink.target = "_blank";
      downloadLink.classList.add("p-button--positive");
      requestBUttonContainer.appendChild(downloadLink);
    });
    closeModalButton.click();
  } else {
    inputContainer.classList.add("is-error");
    errorMessage.innerText = response.message;
  }

  loadingIcon.classList.add("u-hide");
  buttons.forEach((button) => {
    button.disabled = false;
  });
}

const requestAssessmentForm = document.getElementById("request-assessment-form");
/** @type {HTMLInputElement} */
const input = requestAssessmentForm.querySelector("#request-assessment-email");
/** @type {Element} */
const inputContainer = input.parentNode;
/** @type {HTMLElement} */
const errorMessage = requestAssessmentForm.querySelector("#exampleInputErrorMessage");
/** @type {NodeListOf<HTMLButtonElement>} */
const buttons = requestAssessmentForm.querySelectorAll("footer button");
const loadingIcon = requestAssessmentForm.querySelector(".p-icon--spinner");
const requestAssessmentSubmitButton = requestAssessmentForm.querySelector(
  "#request-assessment-submit"
);
/** @type {HTMLElement} */
const closeModalButton = requestAssessmentForm.querySelector(".p-modal__close");
const requestButtonContainer = document.getElementById(
  "reportRequestContainer"
);

requestAssessmentSubmitButton.addEventListener("click", (e) => {
  e.preventDefault();
  runGet();
  fetch(requestAssessmentForm.dataset.action, {
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
    requestButtonContainer.innerHTML = "";
    attachments.forEach((attachment) => {
      // <p style="padding-left: 2.5rem;" class="u-no-margin--bottom"><a href="{{ application['gia_feedback'].url }}" download>Download your GIA feedback document <i class="p-icon--begin-downloading"></i></a></p>
      const downloadContainer = document.createElement("p");
      const downloadLink = document.createElement("a");
      downloadLink.innerHTML = `Download your candidate report <i class="p-icon--begin-downloading"></i>`;
      downloadLink.download = true;
      downloadLink.href = attachment.url;
      downloadLink.target = "_blank";
      downloadContainer.appendChild(downloadLink);
      requestButtonContainer.appendChild(downloadContainer);
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

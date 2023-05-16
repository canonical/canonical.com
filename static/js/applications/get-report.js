const form = document.getElementById("request-assessment-form");
const input = form.querySelector("#request-assessment-email");
const inputContainer = input.parentNode;
const errorMessage = form.querySelector("#exampleInputErrorMessage");
const buttons = form.querySelectorAll("footer button");
const loadingIcon = form.querySelector(".p-icon--spinner");
const submitButton = form.querySelector("#request-assessment-submit");
const closeModalButton = form.querySelector(".p-modal__close");
const requestButtonContainer = document.getElementById(
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

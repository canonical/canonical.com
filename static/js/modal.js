function initVacanciesModal() {
  var modalClose = document.querySelector(".js-vacancies-modal__close");
  var modalElement = document.querySelector(".js-vacancies-modal");
  var modalOpen = document.querySelector(".js-vacancies-modal__open");
  var modalForm = document.querySelector(".js-vacancies-modal__form");
  var selectedRolesList = document.querySelector(
    ".js-vacancies-modal__active-roles"
  );
  var vacanciesList = document.querySelector(".js-vacancies-modal__vacancies");

  if (modalElement) {
    attachEvents();
    setSelectedVacancies();
  }

  function attachEvents() {
    modalOpen.addEventListener("click", function () {
      setSelectedVacancies();
      modalElement.classList.remove("u-hide");
    });

    modalClose.addEventListener("click", function (e) {
      e.preventDefault();
      modalElement.classList.add("u-hide");
    });

    modalElement.addEventListener("click", function (e) {
      if (e.target === modalElement) {
        modalElement.classList.add("u-hide");
      }
    });

    modalForm.addEventListener("submit", function (e) {
      e.preventDefault();
      updateRoles();
      modalElement.classList.add("u-hide");
    });
  }

  function buildCheckbox(id) {
    var input = document.createElement("input");

    input.type = "checkbox";
    input.name = "roles";
    input.id = "role" + id;
    input.checked = true;

    return input;
  }

  function buildLabel(id, text) {
    var label = document.createElement("label");
    var labelText = document.createTextNode(text);

    label.htmlFor = "role" + id;
    label.appendChild(labelText);

    console.log(label);

    return label;
  }

  function setSelectedVacancies() {
    var selectedRoles = selectedRolesList.querySelectorAll("input:checked");

    [].forEach.call(selectedRoles, function (role) {
      var idString = role.getAttribute("id");
      var id = idString.replace("role", "");
      var targetInput = document.querySelector("#vacancy" + id);

      if (targetInput) {
        targetInput.setAttribute("checked", true);
      }
    });
  }

  function updateRoles() {
    var selectedVacancies = vacanciesList.querySelectorAll("input:checked");
    selectedRolesList.innerHTML = "";

    [].forEach.call(selectedVacancies, function (role) {
      var idString = role.getAttribute("id");
      var labelString = vacanciesList.querySelector(
        'label[for="' + idString + '"]'
      ).innerHTML;
      var id = idString.replace("vacancy", "");
      var checkbox = buildCheckbox(id);
      var label = buildLabel(id, labelString);

      selectedRolesList.append(checkbox, label);
    });
  }
}

initVacanciesModal();

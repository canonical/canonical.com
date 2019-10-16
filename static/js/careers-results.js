(function () {
  const rolesListContainer = document.querySelector(".js-roles-list--container");
  const rolesApplyContainer = document.querySelector(".js-roles-apply--container");
  const applyButton = document.querySelector(".js-roles-list--apply-button");
  const addRolesButton = document.querySelector(".js-roles-apply--add-button");
  const selectableJobsList = document.querySelectorAll(".js-roles-list--select");
  const selectedJobsApply = document.querySelectorAll(".js-roles-apply--select");
  const jobIdListInput = document.querySelector("#applicationJobIdList");
  const jobTitleListInput = document.querySelector("#applicationJobTitleList");
  const backbutton = document.querySelector(".js-back-button");

  var selectedJobs = [];

  if (backbutton) {
    backbutton.addEventListener("click", function (e) {
      e.preventDefault();
      if (rolesListContainer && rolesListContainer) {
        rolesListContainer.classList.remove("u-hide");
        rolesApplyContainer.classList.add("u-hide");
      }
    })
  }

  if (applyButton) {
    applyButton.addEventListener("click", function (e) {
      e.preventDefault();
      if (selectedJobsApply) {
        selectedJobsApply.forEach(function (job) {
          const inputElement = job.firstElementChild;
          job.classList.remove("u-hide");
          inputElement.checked = true;
          if (!selectedJobs.some(el => el.id === inputElement.id.split("-")[0])) {
            job.classList.add("u-hide");
            inputElement.checked = false;
          }
        });
      }
      if (jobIdListInput && jobTitleListInput) {
        jobIdListInput.value = convertObjectToString("id", selectedJobs);
        jobTitleListInput.value = convertObjectToString("title", selectedJobs);
      }
      if (rolesListContainer && rolesListContainer) {
        rolesListContainer.classList.add("u-hide");
        rolesApplyContainer.classList.remove("u-hide");
      }
    });
  }
  if (addRolesButton) {
    addRolesButton.addEventListener("click", function () {
      selectableJobsList.forEach(function (job) {
        job.checked = true;
        if (!selectedJobs.some(el => el.id === job.id)) {
          job.checked = false;
        }
      });
      if (rolesListContainer && rolesListContainer) {
        rolesListContainer.classList.remove("u-hide");
        rolesApplyContainer.classList.add("u-hide");
      }
    });
  }

  if (selectableJobsList) {
    selectableJobsList.forEach(function (job) {
      job.addEventListener("change", function (event) {
        if (event.target.checked) {
          selectedJobs.push({ id: event.target.id, title: event.target.name });
        } else {
          selectedJobs = selectedJobs.filter(function (value) {
            return !(value.id === event.target.id);
          });
        }
      });
    });
  }

  if (selectedJobsApply) {
    selectedJobsApply.forEach(function (job) {
      job.firstElementChild.addEventListener("click", function (event) {
        if (event.target.checked) {
          selectedJobs.push({ id: event.target.id.split("-")[0], title: event.target.name });
        } else {
          selectedJobs = selectedJobs.filter(function (value) {
            return !(value.id === event.target.id.split("-")[0]);
          });
        }
        if (jobIdListInput && jobTitleListInput) {
          jobIdListInput.value = convertObjectToString("id", selectedJobs);
          jobTitleListInput.value = convertObjectToString("title", selectedJobs);
        }
      });
    });
  }

  function convertObjectToString(type, selectedJobs) {
    if (type === "id") {
      var idsArray = [];
      selectedJobs.forEach(function (el) {
        idsArray.push(el.id);
      });
      return idsArray.join();
    } else if (type === "title") {
      var titlesArray = [];
      selectedJobs.forEach(function (el) {
        titlesArray.push(el.title);
      });
      return titlesArray.join();
    } else {
      return "";
    }
  }

  function fileValidation() {
    var fileInput = document.getElementById('resume');
    if (fileInput) {
      var filePath = fileInput.value;
      var allowedExtensions = /(\.pdf|\.doc|\.docx|\.txt|\.rtf)$/i;
      if (!allowedExtensions.exec(filePath)) {
        alert('Invalid file format selected. Allowed formats are: pdf, doc, docx, txt, rtf');
        fileInput.value = '';
        return false;
      }
    }
  }
})();
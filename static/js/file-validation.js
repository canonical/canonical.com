(function () {
  const allowedExtensions = /(\.pdf|\.doc|\.docx|\.txt|\.rtf)$/i;
  const maxAllowedSize = 1048576;
  const resumeFileInput = document.getElementById("resume");
  const coverLetterFileInput = document.getElementById("cover_letter");

  const validateFile = (inputElement) => {
    const filePath = inputElement.value;
    const fileSize = inputElement.files[0].size;
    if (!allowedExtensions.exec(filePath)) {
      alert(
        "Invalid file format selected. Allowed formats are: pdf, doc, docx, txt, rtf"
      );
      inputElement.value = "";
    }
    if (fileSize >= maxAllowedSize) {
      alert("Invalid file size. Maximum file size 1MB.");
      inputElement.value = "";
    }
  };

  window.fileValidation = {
    allowedExtensions,
    maxAllowedSize,
    validateFile,
  };

  if (resumeFileInput) {
    resumeFileInput.addEventListener("change", function () {
      validateFile(resumeFileInput);
    });
  }

  if (coverLetterFileInput) {
    coverLetterFileInput.addEventListener("change", function () {
      validateFile(coverLetterFileInput);
    });
  }
})();

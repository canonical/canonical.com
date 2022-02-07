(function () {
  const allowedExtensions = /(\.pdf|\.doc|\.docx|\.txt|\.rtf)$/i;
  const maxAllowedSize = 1048576;
  const resumeFileInput = document.getElementById("resume");
  const coverLetterFileInput = document.getElementById("cover_letter");

  if (resumeFileInput) {
    resumeFileInput.addEventListener("change", function () {
      const filePath = resumeFileInput.value;
      const fileSize = resumeFileInput.files[0].size;
      if (!allowedExtensions.exec(filePath)) {
        alert("Invalid file format selected. Allowed formats are: pdf, doc, docx, txt, rtf");
        resumeFileInput.value = "";
      }
      if (fileSize >= maxAllowedSize) {
        alert("Invalid file size. Maximum file size 1MB.");
        resumeFileInput.value = "";
      }
    });
  }

  if (coverLetterFileInput) {
    coverLetterFileInput.addEventListener("change", function () {
      const filePath = coverLetterFileInput.value;
      const fileSize = coverLetterFileInput.files[0].size;
      if (!allowedExtensions.exec(filePath)) {
        alert("Invalid file format selected. Allowed formats are: pdf, doc, docx, txt, rtf");
        coverLetterFileInput.value = "";
      }
      if (fileSize >= maxAllowedSize) {
        alert("Invalid file size. Maximum file size 1MB.");
        coverLetterFileInput.value = "";
      }
    });
  }
})();

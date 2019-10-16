(function () {
  const allowedExtensions = /(\.pdf|\.doc|\.docx|\.txt|\.rtf)$/i;
  const resumeFileInput = document.getElementById('resume');
  const coverLetterFileInput = document.getElementById('cover_letter');

  if (resumeFileInput) {
    resumeFileInput.addEventListener("change", function () {
      const filePath = resumeFileInput.value;
      if (!allowedExtensions.exec(filePath)) {
        alert('Invalid file format selected. Allowed formats are: pdf, doc, docx, txt, rtf');
        resumeFileInput.value = '';
      }
    });
  }

  if (coverLetterFileInput) {
    coverLetterFileInput.addEventListener("change", function () {
      const filePath = coverLetterFileInput.value;
      if (!allowedExtensions.exec(filePath)) {
        alert('Invalid file format selected. Allowed formats are: pdf, doc, docx, txt, rtf');
        coverLetterFileInput.value = '';
      }
    });
  }
})();

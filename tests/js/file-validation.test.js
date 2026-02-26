/** @jest-environment jsdom */

import "../../static/js/file-validation.js";

describe("file-validation", () => {
  let validateFile;
  let allowedExtensions;
  let maxAllowedSize;

  beforeEach(() => {
    // Get exported functions from window.fileValidation
    validateFile = window.fileValidation.validateFile;
    allowedExtensions = window.fileValidation.allowedExtensions;
    maxAllowedSize = window.fileValidation.maxAllowedSize;

    // Mock alert
    global.alert = jest.fn();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  // Helper function to create a mock file input
  const createMockFileInput = (filename, fileSize) => {
    const input = {
      value: filename,
      files: [{ size: fileSize, name: filename }],
    };
    return input;
  };

  describe("File format validation", () => {
    it("should accept .pdf files", () => {
      const input = createMockFileInput("resume.pdf", 500000);
      validateFile(input);

      expect(global.alert).not.toHaveBeenCalled();
      expect(input.value).toBe("resume.pdf");
    });

    it("should accept .doc files", () => {
      const input = createMockFileInput("resume.doc", 500000);
      validateFile(input);

      expect(global.alert).not.toHaveBeenCalled();
      expect(input.value).toBe("resume.doc");
    });

    it("should accept .docx files", () => {
      const input = createMockFileInput("resume.docx", 500000);
      validateFile(input);

      expect(global.alert).not.toHaveBeenCalled();
      expect(input.value).toBe("resume.docx");
    });

    it("should accept .txt files", () => {
      const input = createMockFileInput("resume.txt", 500000);
      validateFile(input);

      expect(global.alert).not.toHaveBeenCalled();
      expect(input.value).toBe("resume.txt");
    });

    it("should accept .rtf files", () => {
      const input = createMockFileInput("resume.rtf", 500000);
      validateFile(input);

      expect(global.alert).not.toHaveBeenCalled();
      expect(input.value).toBe("resume.rtf");
    });

    it("should reject .jpg files", () => {
      const input = createMockFileInput("resume.jpg", 500000);
      validateFile(input);

      expect(global.alert).toHaveBeenCalledWith(
        "Invalid file format selected. Allowed formats are: pdf, doc, docx, txt, rtf"
      );
      expect(input.value).toBe("");
    });

    it("should reject .png files", () => {
      const input = createMockFileInput("resume.png", 500000);
      validateFile(input);

      expect(global.alert).toHaveBeenCalledWith(
        "Invalid file format selected. Allowed formats are: pdf, doc, docx, txt, rtf"
      );
      expect(input.value).toBe("");
    });

    it("should reject .exe files", () => {
      const input = createMockFileInput("resume.exe", 500000);
      validateFile(input);

      expect(global.alert).toHaveBeenCalledWith(
        "Invalid file format selected. Allowed formats are: pdf, doc, docx, txt, rtf"
      );
    });

    it("should be case insensitive for file extensions", () => {
      const input = createMockFileInput("resume.PDF", 500000);
      validateFile(input);

      expect(global.alert).not.toHaveBeenCalled();
      expect(input.value).toBe("resume.PDF");
    });

    it("should handle file paths with directories", () => {
      const input = createMockFileInput("C:\\Users\\test\\resume.pdf", 500000);
      validateFile(input);

      expect(global.alert).not.toHaveBeenCalled();
    });
  });

  describe("File size validation", () => {
    it("should accept files under 1MB", () => {
      const input = createMockFileInput("resume.pdf", 500000);
      validateFile(input);

      expect(global.alert).not.toHaveBeenCalled();
      expect(input.value).toBe("resume.pdf");
    });

    it("should reject files at 1MB exactly", () => {
      const input = createMockFileInput("resume.pdf", 1048576);
      validateFile(input);

      expect(global.alert).toHaveBeenCalledWith(
        "Invalid file size. Maximum file size 1MB."
      );
      expect(input.value).toBe("");
    });

    it("should reject files over 1MB", () => {
      const input = createMockFileInput("resume.pdf", 2097152);
      validateFile(input);

      expect(global.alert).toHaveBeenCalledWith(
        "Invalid file size. Maximum file size 1MB."
      );
      expect(input.value).toBe("");
    });

    it("should reject files slightly over 1MB", () => {
      const input = createMockFileInput("resume.pdf", 1048577);
      validateFile(input);

      expect(global.alert).toHaveBeenCalledWith(
        "Invalid file size. Maximum file size 1MB."
      );
    });

    it("should accept very small files", () => {
      const input = createMockFileInput("resume.txt", 1024);
      validateFile(input);

      expect(global.alert).not.toHaveBeenCalled();
      expect(input.value).toBe("resume.txt");
    });

    it("should accept files close to 1MB limit", () => {
      const input = createMockFileInput("resume.pdf", 1048000);
      validateFile(input);

      expect(global.alert).not.toHaveBeenCalled();
      expect(input.value).toBe("resume.pdf");
    });
  });

  describe("Multiple validation errors", () => {
    it("should handle invalid format and show alert", () => {
      const input = createMockFileInput("resume.jpg", 500000);
      validateFile(input);

      expect(global.alert).toHaveBeenCalledWith(
        "Invalid file format selected. Allowed formats are: pdf, doc, docx, txt, rtf"
      );
    });

    it("should prioritize format validation before size validation", () => {
      const input = createMockFileInput("resume.jpg", 2097152);
      validateFile(input);

      // Should only show format error first, then size error
      expect(global.alert).toHaveBeenCalledTimes(2);
      expect(global.alert).toHaveBeenNthCalledWith(
        1,
        "Invalid file format selected. Allowed formats are: pdf, doc, docx, txt, rtf"
      );
      expect(global.alert).toHaveBeenNthCalledWith(
        2,
        "Invalid file size. Maximum file size 1MB."
      );
    });
  });

  describe("Input value clearing", () => {
    it("should clear input value on invalid format", () => {
      const input = createMockFileInput("resume.jpg", 500000);
      expect(input.value).toBe("resume.jpg");
      validateFile(input);
      expect(input.value).toBe("");
    });

    it("should clear input value on invalid size", () => {
      const input = createMockFileInput("resume.pdf", 2097152);
      expect(input.value).toBe("resume.pdf");
      validateFile(input);
      expect(input.value).toBe("");
    });

    it("should not clear input value on valid file", () => {
      const input = createMockFileInput("resume.pdf", 500000);
      validateFile(input);
      expect(input.value).toBe("resume.pdf");
    });
  });

  describe("File extension regex", () => {
    it("should match pdf extension", () => {
      expect(allowedExtensions.test("file.pdf")).toBe(true);
    });

    it("should match doc extension", () => {
      expect(allowedExtensions.test("file.doc")).toBe(true);
    });

    it("should match docx extension", () => {
      expect(allowedExtensions.test("file.docx")).toBe(true);
    });

    it("should match txt extension", () => {
      expect(allowedExtensions.test("file.txt")).toBe(true);
    });

    it("should match rtf extension", () => {
      expect(allowedExtensions.test("file.rtf")).toBe(true);
    });

    it("should be case insensitive", () => {
      expect(allowedExtensions.test("file.PDF")).toBe(true);
      expect(allowedExtensions.test("file.Pdf")).toBe(true);
      expect(allowedExtensions.test("file.pDf")).toBe(true);
    });

    it("should not match invalid extensions", () => {
      expect(allowedExtensions.test("file.jpg")).toBe(false);
      expect(allowedExtensions.test("file.png")).toBe(false);
      expect(allowedExtensions.test("file.exe")).toBe(false);
      expect(allowedExtensions.test("file.zip")).toBe(false);
    });

    it("should require extension at end of string", () => {
      expect(allowedExtensions.test("file.pdf.exe")).toBe(false);
      expect(allowedExtensions.test("pdf")).toBe(false);
    });
  });

  describe("Constants", () => {
    it("should define correct max allowed size", () => {
      expect(maxAllowedSize).toBe(1048576);
    });

    it("should define allowed extensions regex", () => {
      expect(allowedExtensions).toBeInstanceOf(RegExp);
    });
  });
});

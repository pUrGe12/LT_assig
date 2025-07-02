document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("uploadForm");
  const pdfInput = document.getElementById("pdfInput");
  const uploadLabelSpan = document.querySelector(".upload-label span");
  const resultBox = document.getElementById("result");

  pdfInput.addEventListener("change", () => {
    if (pdfInput.files.length > 0) {
      uploadLabelSpan.textContent = pdfInput.files[0].name;
    } else {
      uploadLabelSpan.textContent = "Add PDF";
    }
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("pdf", pdfInput.files[0]);

    try {
      const res = await fetch("/api/documents/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (res.ok) {
        resultBox.style.color = "var(--success)";
        resultBox.textContent = `Upload done - UniqueID: ${data.id}`;
      } else {
        resultBox.style.color = "var(--error)";
        resultBox.textContent = `Some error happened: ${data.error}`;
      }
    } catch (err) {
      resultBox.style.color = "var(--error)";
      resultBox.textContent = `Some more error happened: ${err.message}`;
    }
  });
});
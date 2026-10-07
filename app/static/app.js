const form = document.getElementById("upload-form");
const imageInput = document.getElementById("leaf-image");
const dropzone = document.getElementById("dropzone");
const previewWrap = document.getElementById("preview-wrap");
const preview = document.getElementById("preview");
const previewName = document.getElementById("preview-name");
const removeButton = document.getElementById("remove-image");
const help = document.getElementById("file-help");
const selectionStatus = document.getElementById("selection-status");
const submitButton = document.getElementById("submit-button");
const submitLabel = document.getElementById("submit-label");
let previewUrl = null;

function clearPreview() {
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  previewUrl = null;
  if (preview) preview.removeAttribute("src");
  if (previewWrap) previewWrap.hidden = true;
  if (imageInput) imageInput.value = "";
  if (selectionStatus) selectionStatus.textContent = "";
  if (help) help.innerHTML = 'JPG, PNG or WebP <span>·</span> up to 10 MB';
}

function chooseFile(file) {
  if (!file || !imageInput) return;
  const supported = ["image/jpeg", "image/png", "image/webp"].includes(file.type)
    || /\.(jpe?g|png|webp)$/i.test(file.name);
  if (!supported) {
    clearPreview();
    if (selectionStatus) selectionStatus.textContent = "Choose a JPG, PNG or WebP image.";
    return;
  }
  if (file.size > 10 * 1024 * 1024) {
    clearPreview();
    if (selectionStatus) selectionStatus.textContent = "This image is larger than 10 MB. Choose a smaller file.";
    return;
  }

  if (previewUrl) URL.revokeObjectURL(previewUrl);
  previewUrl = URL.createObjectURL(file);
  preview.src = previewUrl;
  preview.alt = `Preview of ${file.name}`;
  previewName.textContent = file.name;
  previewWrap.hidden = false;
  if (help) help.textContent = `${(file.size / (1024 * 1024)).toFixed(2)} MB selected`;
  if (selectionStatus) selectionStatus.textContent = "Image ready to analyze.";
}

if (imageInput) {
  imageInput.addEventListener("change", () => chooseFile(imageInput.files && imageInput.files[0]));
}

if (removeButton) {
  removeButton.addEventListener("click", () => {
    clearPreview();
    if (imageInput && !imageInput.disabled) imageInput.focus();
  });
}

if (dropzone && imageInput) {
  dropzone.addEventListener("keydown", (event) => {
    if ((event.key === "Enter" || event.key === " ") && event.target === dropzone && !imageInput.disabled) {
      event.preventDefault();
      imageInput.click();
    }
  });
  ["dragenter", "dragover"].forEach((eventName) => {
    dropzone.addEventListener(eventName, (event) => {
      event.preventDefault();
      if (!imageInput.disabled) dropzone.classList.add("is-dragging");
    });
  });
  ["dragleave", "dragend"].forEach((eventName) => {
    dropzone.addEventListener(eventName, () => dropzone.classList.remove("is-dragging"));
  });
  dropzone.addEventListener("drop", (event) => {
    event.preventDefault();
    dropzone.classList.remove("is-dragging");
    const file = event.dataTransfer && event.dataTransfer.files[0];
    if (!file || imageInput.disabled) return;
    const transfer = new DataTransfer();
    transfer.items.add(file);
    imageInput.files = transfer.files;
    chooseFile(file);
  });
}

if (form && submitButton && submitLabel) {
  form.addEventListener("submit", (event) => {
    if (!imageInput || !imageInput.files || !imageInput.files[0]) {
      event.preventDefault();
      if (selectionStatus) selectionStatus.textContent = "Choose a leaf photo before continuing.";
      if (dropzone) dropzone.focus();
      return;
    }
    submitButton.disabled = true;
    submitButton.classList.add("is-loading");
    form.setAttribute("aria-busy", "true");
    submitLabel.textContent = "Analyzing image…";
  });
}

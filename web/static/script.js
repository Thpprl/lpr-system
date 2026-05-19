document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const dropzone = document.getElementById("dropzone");
    const fileInput = document.getElementById("file-input");
    const browseBtn = document.getElementById("browse-btn");
    const analyzeBtn = document.getElementById("analyze-btn");
    const spinner = document.getElementById("spinner");
    const emptyState = document.getElementById("empty-state");
    const errorAlert = document.getElementById("error-alert");
    const errorMsg = errorAlert.querySelector(".error-msg");
    const resultsDisplay = document.getElementById("results-display");
    const previewContainer = document.getElementById("preview-container");
    const imagePreview = document.getElementById("image-preview");
    const btnClear = document.getElementById("btn-clear");
    
    // Results DOM Elements
    const plateCrop = document.getElementById("plate-crop");
    const resPlateNumber = document.getElementById("res-plate-number");
    const resProvince = document.getElementById("res-province");
    const resPlateColor = document.getElementById("res-plate-color");
    const resTextColor = document.getElementById("res-text-color");
    const resVehicleType = document.getElementById("res-vehicle-type");

    let selectedFile = null;

    // ==========================================
    // File Upload & Preview Handlers
    // ==========================================

    // Click to select
    browseBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        fileInput.click();
    });

    dropzone.addEventListener("click", () => {
        if (!selectedFile) {
            fileInput.click();
        }
    });

    fileInput.addEventListener("change", (e) => {
        handleFileSelect(e.target.files[0]);
    });

    // Drag & Drop events
    ["dragenter", "dragover"].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.add("dragover");
        }, false);
    });

    ["dragleave", "drop"].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.remove("dragover");
        }, false);
    });

    dropzone.addEventListener("drop", (e) => {
        const dt = e.dataTransfer;
        const file = dt.files[0];
        handleFileSelect(file);
    });

    // Clear selected file
    btnClear.addEventListener("click", (e) => {
        e.stopPropagation();
        resetUploadState();
    });

    function handleFileSelect(file) {
        if (!file) return;

        // Check if it's an image
        if (!file.type.match("image.*")) {
            showError("Invalid file type. Please select an image file.");
            return;
        }

        selectedFile = file;
        
        // Show Image Preview
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            previewContainer.hidden = false;
            analyzeBtn.disabled = false;
            hideError();
        };
        reader.readAsDataURL(file);
    }

    function resetUploadState() {
        selectedFile = null;
        fileInput.value = "";
        imagePreview.src = "#";
        previewContainer.hidden = true;
        analyzeBtn.disabled = true;
        hideError();
        showEmptyState();
    }

    // ==========================================
    // API Integration
    // ==========================================

    analyzeBtn.addEventListener("click", async () => {
        if (!selectedFile) return;

        // UI Loading State
        setLoading(true);
        hideError();
        
        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
            const response = await fetch("/api/predict", {
                method: "POST",
                body: formData
            });

            const result = await response.json();

            if (response.ok && result.success) {
                displayResults(result.data);
            } else {
                throw new Error(result.error || "Failed to analyze image.");
            }
        } catch (error) {
            showError(error.message);
            showEmptyState();
        } finally {
            setLoading(false);
        }
    });

    // ==========================================
    // UI Helpers
    // ==========================================

    function setLoading(isLoading) {
        if (isLoading) {
            analyzeBtn.disabled = true;
            spinner.hidden = false;
            analyzeBtn.querySelector("span").textContent = "Analyzing...";
        } else {
            analyzeBtn.disabled = false;
            spinner.hidden = true;
            analyzeBtn.querySelector("span").textContent = "Analyze Image";
        }
    }

    function displayResults(data) {
        emptyState.hidden = true;
        resultsDisplay.hidden = false;

        // Fill in metadata
        resPlateNumber.textContent = data.plate_number || "ไม่สามารถระบุได้";
        resProvince.textContent = data.province || "ไม่สามารถระบุได้";
        resPlateColor.textContent = data.plate_color || "ไม่สามารถระบุได้";
        resTextColor.textContent = data.text_color || "ไม่สามารถระบุได้";
        resVehicleType.textContent = data.vehicle_type || "ไม่สามารถระบุได้";

        // Display cropped plate image with cache-buster timestamp
        if (data.crop_url) {
            const timestamp = new Date().getTime();
            plateCrop.src = `${data.crop_url}?t=${timestamp}`;
            plateCrop.parentElement.style.display = "flex";
        } else {
            plateCrop.src = "#";
            plateCrop.parentElement.style.display = "none";
        }
    }

    function showEmptyState() {
        emptyState.hidden = false;
        resultsDisplay.hidden = true;
    }

    function showError(message) {
        errorMsg.textContent = message;
        errorAlert.hidden = false;
        resultsDisplay.hidden = true;
        emptyState.hidden = true;
    }

    function hideError() {
        errorAlert.hidden = true;
        errorMsg.textContent = "";
    }
});

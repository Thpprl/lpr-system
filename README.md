# Thai License Plate Recognition (LPR) System

[![Python](https://img.shields.co/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.co/badge/PyTorch-2.1.2-EE4C2C.svg)](https://pytorch.org/)
[![Ultralytics YOLOv8](https://img.shields.co/badge/YOLO-v8.3.0-blueviolet.svg)](https://github.com/ultralytics/ultralytics)
[![HuggingFace](https://img.shields.co/badge/%F0%9F%A4%97-Transformers-yellow.svg)](https://huggingface.co/)
[![PEFT/LoRA](https://img.shields.co/badge/PEFT-LoRA-lightgrey.svg)](https://github.com/huggingface/peft)

A state-of-the-art, dual-stage **Thai License Plate Recognition (LPR)** system. This project merges **YOLOv8 Object Detection** for localization with a **fine-tuned Qwen-VL Vision-Language Model (VLM)** via **LoRA (PEFT)** for high-precision OCR extraction of Thai script, numbers, provinces, and plate colors. 

Includes a CLI tool (supporting single and batch operations with automated evaluations) and a performance benchmarking suite.

---

## 🛠️ System Architecture

The pipeline processes input images through a specialized modular framework:

```
[Input Vehicle Image]
         │
         ▼
   ┌───────────┐
   │  YOLOv8   │ ──► Object Detection & Localization
   └───────────┘
         │
         ▼
[Cropped Plate Crop]
         │
         ▼
   ┌───────────┐
   │  Qwen-VL  │ ──► Fine-tuned VLM (via LoRA Adapter)
   │  VLM OCR  │     Extracts: Plate Text, Province, Colors
   └───────────┘
         │
         ▼
   ┌───────────┐
   │  Post-    │ ──► Rule-based Vehicle Type Classifier
   │  Process  │     (Maps Plate + Text color to legal categories)
   └───────────┘
         │
         ▼
 ┌──────────────┐
 │   CLI Output │ ──► Print format / JSON / CSV File
 └──────────────┘
```

---

## ✨ Features

- **License Plate Localization (YOLOv8):** Detects Thai license plates and crops them for processing.
- **Multimodal OCR (Qwen-VL-2B-Instruct + LoRA):** A vision-language model fine-tuned on Thai plates to extract textual information and identify plate colors directly.
- **Color-to-Vehicle Type Mapping:** Post-processing module that classifies vehicles into legal Thai classes (e.g., *Private Car*, *Public Taxi*, *Government Vehicle*) using background and text color rules.
- **Developer Command Line (CLI):** Modes for `single` image analysis or folder-based `batch` processing.
- **Performance Evaluation Suite:** Script to automatically measure Character Error Rate (CER) and accuracy metrics across ground truth data.

---

## 📂 Project Directory Structure

```
lpr-system/
├── run.py                 # Main entry point (single / batch modes)
├── eval.py                # System evaluation script (CER & Accuracy)
├── requirements.txt       # Dependencies list
├── pipeline/              # Core processing logic
│   ├── pipeline.py        # Orchestrates YOLO -> Qwen -> Post-processing
│   ├── batch.py           # Handles bulk directories processing
│   ├── yolo/              # License plate detection module (YOLOv8)
│   ├── qwen/              # VLM OCR model loader and inference handlers
│   ├── postprocess/       # Vehicle type classifiers and output parsers
│   └── utils/             # File handlers (JSON & CSV savers)
├── models/                # Local model storage (ignored in git)
│   ├── yolo/best.pt       # Fine-tuned YOLOv8 weights
│   └── qwen/checkpoint-400/  # LoRA adapters for Qwen-VL-2B-Instruct
├── test/                  # Test scripts and datasets
└── output/                # Processed crop outputs, JSON, and CSV records
```

---

## 🚀 Installation & Setup

### 1. Clone the Repository & Configure Python
Ensure you are using **Python 3.10**:
```bash
git clone https://github.com/Thpprl/lpr-system.git
cd lpr-system
```

### 2. Set Up Virtual Environment (Recommended)
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On Linux/macOS
source .venv/bin/activate
```

### 3. Install Dependencies
Install PyTorch with CUDA support if you are using an NVIDIA GPU (recommended for VLM inference):
```bash
# Example for CUDA 11.8
pip install torch==2.1.2 torchvision==0.16.2 --index-url https://download.pytorch.org/whl/cu118
# Install the rest of the libraries
pip install -r requirements.txt
```

### 4. Weights Setup
Make sure the models are placed in the correct directories:
- Place the fine-tuned YOLO weights (`best.pt`) in `models/yolo/best.pt`.
- Place the LoRA adapter folder (`checkpoint-400/`) in `models/qwen/checkpoint-400/`.

*Note: Large model weights (`models/`) and outputs (`output/`) are listed in `.gitignore` to avoid large pushes.*

---

## 💻 Usage Guide

### Mode 1: Single Image CLI
Run predictions on a single vehicle image:
```bash
python run.py single path/to/image.jpg
```
Save predictions to `output/json/` and `output/csv/`:
```bash
python run.py single path/to/image.jpg --save
```

### Mode 2: Batch Directory CLI
Run predictions on a folder containing multiple vehicle images:
```bash
python run.py batch path/to/images_folder/ --save
```

### Mode 3: Pipeline Evaluation
To evaluate system performance, place a ground-truth labels sheet in `compare/labels.csv` and run:
```bash
python eval.py
```
This prints the overall summary and saves file-by-file analytics to `eval_detail.csv`.

---

## 📊 Evaluation Summary

Below is an evaluation summary evaluated across a 50-image test set:

| Evaluation Metric | Score | Note / Performance |
| :--- | :---: | :--- |
| **Average Character Error Rate (CER)** | **8.93%** | Very low character mismatch distance |
| **Exact Plate Number Accuracy** | **56.00%** | Exact character and number match |
| **Province Accuracy** | **60.00%** | Correct Thai province mapping |
| **Plate & Text Colors Recognition** | **100.00%** | Normalized matching accuracy |
| **Canonical Vehicle Type Classification**| **100.00%** | Color mapping post-processed accuracy |

---

## ⚖️ License
Distributed under the MIT License. See `LICENSE` for details.

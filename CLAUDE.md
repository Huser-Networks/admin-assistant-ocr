# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a PDF OCR processing application that reads PDF files from configured folders and extracts text using Optical Character Recognition (OCR). The application uses multithreading to process multiple files concurrently.

## Development Setup

### Virtual Environment
The project uses a Python virtual environment located at `ocr-venv/`. Activate it before running:
```bash
# Windows
ocr-venv\Scripts\activate

# Linux/Mac  
source ocr-venv/bin/activate
```

### Required Dependencies
Install from requirements.txt:
```bash
pip install -r requirements.txt
```

Main packages:
- `pytesseract` - Python wrapper for Tesseract OCR
- `pdf2image` - Convert PDF to images
- `Pillow` - Image processing

Note: System dependencies required:
- Tesseract OCR must be installed on the system
- `poppler-utils` (for pdf2image on Linux) or equivalent PDF rendering library

## Running the Application

```bash
python main.py
```

## Architecture

### Core Components

1. **main.py**: Entry point that orchestrates the OCR workflow by loading config, exploring folders, and initiating concurrent processing.

2. **Controllers** (`src/controllers/`):
   - `config_controller.py`: Loads configuration from `src/config/config.json`
   - `file_controller.py`: Explores folders recursively to find files
   - `ocr_controller.py`: Handles PDF to image conversion and OCR processing using pytesseract

3. **Utilities** (`src/utils/`):
   - `concurrent_manager.py`: Manages multithreaded file processing using ThreadPoolExecutor

### Configuration
The application is configured via `src/config/config.json`:
- `scan_folder`: Base folder to scan for PDFs (default: "scan")
- `sub_folders`: List of subfolders to process (default: ["HN"])
- `output_folder`: Where to store results (default: "output")

### Processing Flow
1. Load configuration from JSON (auto-creates default if missing)
2. For each configured subfolder:
   - Recursively find all PDF files in the folder
   - Process files concurrently using ThreadPoolExecutor
   - Each PDF is converted to images, then OCR is applied to extract text
   - Results are saved as text files in the output folder

### Key Features
- **Automatic text extraction and saving**: OCR results are saved as .txt files
- **PDF-only filtering**: Only processes PDF files by default
- **Comprehensive logging**: All operations logged to console and file (logs/ directory)
- **Error handling**: Graceful handling of missing folders, invalid PDFs, and OCR failures
- **Configuration validation**: Auto-creates default config if missing
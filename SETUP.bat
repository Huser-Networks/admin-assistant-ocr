@echo off
REM Installation rapide OCR Assistant

chcp 65001 >nul
cd /d "%~dp0"

echo ====================================
echo   SETUP OCR ASSISTANT
echo ====================================
echo.

REM Verifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python requis. Installez Python depuis python.org
    pause
    exit /b 1
)

echo [OK] Python detecte
echo.

REM Recreer l'environnement virtuel proprement
if exist "ocr-venv" (
    echo Suppression ancien environnement...
    rmdir /s /q ocr-venv
)

echo Creation environnement virtuel...
python -m venv ocr-venv
if errorlevel 1 (
    echo [ERREUR] Impossible de creer l'environnement virtuel
    pause
    exit /b 1
)

echo Installation packages...
ocr-venv\Scripts\python.exe -m pip install --upgrade pip
ocr-venv\Scripts\pip.exe install Pillow pdf2image pytesseract opencv-python numpy

echo.
echo Test rapide...
ocr-venv\Scripts\python.exe -c "import PIL, pdf2image, pytesseract; print('[OK] Packages installes')"
if errorlevel 1 (
    echo [ERREUR] Probleme avec les packages
) else (
    echo.
    echo ====================================
    echo   INSTALLATION REUSSIE !
    echo ====================================
    echo.
    echo Lancez l'application avec: START.bat
)

echo.
pause
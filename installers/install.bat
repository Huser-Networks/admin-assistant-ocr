@echo off
REM Script d'installation complete pour OCR Assistant sur Windows
REM Se lance depuis la racine du projet

chcp 65001 >nul
cd /d "%~dp0"
cd ..

echo ====================================
echo   INSTALLATION OCR ASSISTANT
echo ====================================
echo.

REM Verifier si Python est installe
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH
    echo Veuillez installer Python depuis https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python est installe
echo.

REM Verifier l'environnement virtuel
if exist "ocr-venv\Scripts\python.exe" (
    REM Tester si l'environnement virtuel fonctionne
    ocr-venv\Scripts\python.exe --version >nul 2>&1
    if errorlevel 1 (
        echo [ERREUR] L'environnement virtuel existe mais ne fonctionne pas
        echo Il a probablement ete cree avec une autre version de Python
        echo.
        echo Suppression de l'ancien environnement...
        rmdir /s /q ocr-venv
        echo Creation d'un nouvel environnement virtuel...
        python -m venv ocr-venv
        if errorlevel 1 (
            echo [ERREUR] Impossible de creer l'environnement virtuel
            pause
            exit /b 1
        )
        echo [OK] Nouvel environnement virtuel cree
    ) else (
        echo [OK] Environnement virtuel existe et fonctionne
    )
) else (
    echo Creation de l'environnement virtuel...
    python -m venv ocr-venv
    if errorlevel 1 (
        echo [ERREUR] Impossible de creer l'environnement virtuel
        pause
        exit /b 1
    )
    echo [OK] Environnement virtuel cree
)

echo.

REM Utiliser pip de l'environnement virtuel
echo Mise a jour de pip...
ocr-venv\Scripts\python.exe -m pip install --upgrade pip

REM Installer les dependances depuis requirements.txt
echo.
echo Installation des dependances Python...
if exist "requirements.txt" (
    ocr-venv\Scripts\pip.exe install -r requirements.txt
) else (
    echo [ERREUR] requirements.txt non trouve
    echo Installation manuelle des packages essentiels...
    ocr-venv\Scripts\pip.exe install Pillow pdf2image pytesseract opencv-python numpy
)

REM Lancer le script de verification avec l'environnement virtuel
echo.
echo Verification de l'installation...
if exist "installers\install_dependencies.py" (
    ocr-venv\Scripts\python.exe installers\install_dependencies.py
) else (
    echo Script de verification non trouve, verification manuelle...
    ocr-venv\Scripts\python.exe -c "import PIL, pdf2image, pytesseract; print('Packages essentiels installes')"
)

echo.
echo ====================================
echo   INSTALLATION TERMINEE
echo ====================================
echo.
echo Pour lancer l'application:
echo   - Double-cliquez sur START.bat
echo   - Ou executez: python bin\launch.py
echo.
pause
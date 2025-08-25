@echo off
REM Lanceur pour OCR Assistant GUI sur Windows
REM Active l'environnement virtuel et lance l'interface

echo ====================================
echo    OCR Assistant - Interface GUI
echo ====================================
echo.

REM Activer l'environnement virtuel
if exist "ocr-venv\Scripts\activate.bat" (
    echo Activation de l'environnement virtuel...
    call ocr-venv\Scripts\activate.bat
) else (
    echo [ERREUR] Environnement virtuel non trouvé!
    echo Veuillez créer l'environnement virtuel avec:
    echo    python -m venv ocr-venv
    echo    ocr-venv\Scripts\activate
    echo    pip install -r requirements.txt
    pause
    exit /b 1
)

REM Lancer l'interface graphique
echo Lancement de l'interface...
python ocr_gui.py

REM Si erreur, attendre avant de fermer
if errorlevel 1 (
    echo.
    echo [ERREUR] L'interface n'a pas pu démarrer.
    pause
)
@echo off
REM Lanceur principal OCR Assistant
REM Redirige vers le bon script dans bin/

cd /d "%~dp0"

if not exist "ocr-venv\Scripts\python.exe" (
    echo ====================================
    echo   PREMIERE INSTALLATION REQUISE
    echo ====================================
    echo.
    echo L'environnement virtuel n'existe pas.
    echo Lancement de l'installation...
    echo.
    call installers\install.bat
    echo.
)

REM Lancer l'application avec l'environnement virtuel
ocr-venv\Scripts\python.exe gui\ocr_gui.py

if errorlevel 1 (
    echo.
    echo [ERREUR] Problème détecté
    echo.
    echo Options:
    echo 1. Exécutez: installers\recreate_venv.bat
    echo 2. Ou: installers\check_python.bat pour diagnostic
    pause
)
@echo off
REM Lanceur principal pour OCR Assistant sur Windows
REM Utilise toujours l'environnement virtuel ocr-venv

cd /d "%~dp0"

echo ====================================
echo    OCR Assistant - Lancement
echo ====================================
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "ocr-venv\Scripts\python.exe" (
    echo [ERREUR] Environnement virtuel non trouvé!
    echo.
    echo Exécutez d'abord: installers\install_all.bat
    echo.
    pause
    exit /b 1
)

REM Utiliser Python de l'environnement virtuel directement
echo Lancement avec l'environnement virtuel...
ocr-venv\Scripts\python.exe gui\ocr_gui.py

if errorlevel 1 (
    echo.
    echo [ERREUR] L'application n'a pas pu démarrer.
    echo Vérifiez que toutes les dépendances sont installées.
    pause
)
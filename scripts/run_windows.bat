@echo off
echo === Démarrage OCR Assistant ===
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "ocr-venv\Scripts\activate.bat" (
    echo [ERREUR] L'environnement virtuel n'existe pas !
    echo Lancez d'abord: scripts\install_windows.bat
    pause
    exit /b 1
)

REM Activer l'environnement virtuel
call ocr-venv\Scripts\activate.bat

REM Lancer l'application
python main.py

pause
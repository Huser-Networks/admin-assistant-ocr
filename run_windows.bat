@echo off
echo === Démarrage OCR Assistant ===
echo.

REM Activer l'environnement virtuel
call ocr-venv\Scripts\activate.bat

REM Lancer l'application
python main.py

pause
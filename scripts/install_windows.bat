@echo off
echo === Installation OCR Assistant sur Windows ===
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installé ou pas dans le PATH
    echo Téléchargez Python depuis: https://www.python.org/downloads/
    echo Assurez-vous de cocher "Add Python to PATH" lors de l'installation
    pause
    exit /b 1
)

echo [OK] Python trouvé
echo.

REM Créer l'environnement virtuel
echo Création de l'environnement virtuel...
python -m venv ocr-venv

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call ocr-venv\Scripts\activate.bat

REM Installer les dépendances
echo Installation des dépendances Python...
pip install --upgrade pip
pip install -r requirements.txt

REM Créer les dossiers nécessaires
echo Création des dossiers...
if not exist "scan\HN" mkdir scan
if not exist "output" mkdir output
if not exist "logs" mkdir logs

echo.
echo === Installation Python terminée ===
echo.
echo IMPORTANT: Vous devez encore installer:
echo.
echo 1. TESSERACT OCR:
echo    - Télécharger: https://github.com/UB-Mannheim/tesseract/wiki
echo    - Installer et noter le chemin (ex: C:\Program Files\Tesseract-OCR)
echo.
echo 2. POPPLER (pour PDF):
echo    - Télécharger: https://github.com/oschwartz10612/poppler-windows/releases
echo    - Extraire dans C:\Tools\poppler
echo    - Ajouter C:\Tools\poppler\Library\bin au PATH
echo.
echo Pour lancer l'application:
echo    ocr-venv\Scripts\activate
echo    python main.py
echo.
pause
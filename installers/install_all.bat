@echo off
REM Script d'installation complète pour OCR Assistant sur Windows

echo ====================================
echo   INSTALLATION OCR ASSISTANT
echo ====================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou pas dans le PATH
    echo Veuillez installer Python depuis https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python est installé
echo.

REM Créer l'environnement virtuel si nécessaire
if not exist "ocr-venv" (
    echo Création de l'environnement virtuel...
    python -m venv ocr-venv
    if errorlevel 1 (
        echo [ERREUR] Impossible de créer l'environnement virtuel
        pause
        exit /b 1
    )
    echo [OK] Environnement virtuel créé
) else (
    echo [OK] Environnement virtuel existe déjà
)

echo.

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call ocr-venv\Scripts\activate.bat

REM Mettre à jour pip
echo.
echo Mise à jour de pip...
python -m pip install --upgrade pip

REM Installer les dépendances depuis requirements.txt
echo.
echo Installation des dépendances Python...
pip install -r requirements.txt

REM Lancer le script de vérification
echo.
echo Vérification de l'installation...
python install_dependencies.py

echo.
echo ====================================
echo   INSTALLATION TERMINÉE
echo ====================================
echo.
echo Pour lancer l'application:
echo   - Double-cliquez sur launch_gui.bat
echo   - Ou exécutez: python launch_gui.py
echo.
pause
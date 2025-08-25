@echo off
REM Script d'installation complète pour OCR Assistant sur Windows
REM Se lance depuis la racine du projet

cd /d "%~dp0"

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

REM Vérifier l'environnement virtuel
if exist "ocr-venv\Scripts\python.exe" (
    REM Tester si l'environnement virtuel fonctionne
    ocr-venv\Scripts\python.exe --version >nul 2>&1
    if errorlevel 1 (
        echo [ERREUR] L'environnement virtuel existe mais ne fonctionne pas
        echo Il a probablement été créé avec une autre version de Python
        echo.
        echo Suppression de l'ancien environnement...
        rmdir /s /q ocr-venv
        echo Création d'un nouvel environnement virtuel...
        python -m venv ocr-venv
        if errorlevel 1 (
            echo [ERREUR] Impossible de créer l'environnement virtuel
            pause
            exit /b 1
        )
        echo [OK] Nouvel environnement virtuel créé
    ) else (
        echo [OK] Environnement virtuel existe et fonctionne
    )
) else (
    echo Création de l'environnement virtuel...
    python -m venv ocr-venv
    if errorlevel 1 (
        echo [ERREUR] Impossible de créer l'environnement virtuel
        pause
        exit /b 1
    )
    echo [OK] Environnement virtuel créé
)

echo.

REM Utiliser pip de l'environnement virtuel
echo Mise à jour de pip...
ocr-venv\Scripts\python.exe -m pip install --upgrade pip

REM Installer les dépendances depuis requirements.txt
echo.
echo Installation des dépendances Python...
ocr-venv\Scripts\pip.exe install -r requirements.txt

REM Lancer le script de vérification avec l'environnement virtuel
echo.
echo Vérification de l'installation...
ocr-venv\Scripts\python.exe installers\install_dependencies.py

echo.
echo ====================================
echo   INSTALLATION TERMINÉE
echo ====================================
echo.
echo Pour lancer l'application:
echo   - Double-cliquez sur launch.bat
echo   - Ou exécutez: python launch.py
echo.
pause
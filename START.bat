@echo off
REM OCR Assistant - Lanceur intelligent
REM Verifie tout d'abord, puis propose les corrections si necessaire

chcp 65001 >nul
setlocal EnableDelayedExpansion
cd /d "%~dp0"

echo ====================================
echo      OCR ASSISTANT
echo ====================================
echo.

REM Variables globales
set "venv_name=ocr-venv"
set "all_ok=1"

echo Verification de l'installation...
echo.

REM === VERIFICATION 1: Python ===
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe
    set "all_ok=0"
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set "python_version=%%i"
    echo [OK] Python !python_version! detecte
)

REM === VERIFICATION 2: Environnement virtuel ===
if exist "%venv_name%\Scripts\python.exe" (
    %venv_name%\Scripts\python.exe --version >nul 2>&1
    if errorlevel 1 (
        echo [ERREUR] Environnement virtuel defectueux
        set "all_ok=0"
    ) else (
        echo [OK] Environnement virtuel fonctionnel
    )
) else (
    echo [ERREUR] Environnement virtuel manquant
    set "all_ok=0"
)

REM === VERIFICATION 3: Packages Python ===
if exist "%venv_name%\Scripts\python.exe" (
    set "packages_ok=1"
    
    %venv_name%\Scripts\python.exe -c "import PIL" >nul 2>&1
    if errorlevel 1 set "packages_ok=0"
    
    %venv_name%\Scripts\python.exe -c "import pdf2image" >nul 2>&1
    if errorlevel 1 set "packages_ok=0"
    
    %venv_name%\Scripts\python.exe -c "import pytesseract" >nul 2>&1
    if errorlevel 1 set "packages_ok=0"
    
    %venv_name%\Scripts\python.exe -c "import cv2" >nul 2>&1
    if errorlevel 1 set "packages_ok=0"
    
    %venv_name%\Scripts\python.exe -c "import numpy" >nul 2>&1
    if errorlevel 1 set "packages_ok=0"
    
    if "!packages_ok!"=="1" (
        echo [OK] Packages Python installes
    ) else (
        echo [ERREUR] Packages Python manquants
        set "all_ok=0"
    )
)

REM === VERIFICATION 4: Structure de dossiers ===
set "folders_ok=1"
if not exist "gui\ocr_gui.py" (
    echo [ERREUR] Interface graphique manquante
    set "folders_ok=0"
    set "all_ok=0"
)
if not exist "src\controllers" (
    echo [ERREUR] Dossier controllers manquant
    set "folders_ok=0"
    set "all_ok=0"
)
if "!folders_ok!"=="1" echo [OK] Structure de fichiers complete

REM === VERIFICATION 5: Configuration ===
if exist "src\config\config.json" (
    echo [OK] Configuration presente
) else (
    echo [ATTENTION] Configuration de base manquante
    set "config_missing=1"
)

echo.

REM === SI TOUT EST OK, LANCER DIRECTEMENT ===
if "%all_ok%"=="1" (
    echo ====================================
    echo   LANCEMENT DE L'APPLICATION
    echo ====================================
    echo.
    
    REM Creer les dossiers de travail si necessaires
    if not exist "scan" mkdir scan >nul 2>&1
    if not exist "output" mkdir output >nul 2>&1
    if not exist "logs" mkdir logs >nul 2>&1
    
    REM Configuration initiale si premiere fois
    if defined config_missing (
        call :create_basic_config
    )
    
    echo Lancement avec l'environnement: %venv_name%
    echo.
    %venv_name%\Scripts\python.exe gui\ocr_gui.py
    goto :end_with_error_check
)

REM === SINON, PROPOSER LES CORRECTIONS ===
echo ====================================
echo   PROBLEMES DETECTES
echo ====================================
echo.
echo Des problemes ont ete detectes avec votre installation.
echo.

REM Gestion des erreurs Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [CRITIQUE] Python n'est pas installe ou accessible.
    echo.
    echo Veuillez installer Python depuis: https://www.python.org/
    echo Puis relancez ce script.
    echo.
    pause
    exit /b 1
)

echo Voulez-vous corriger automatiquement ces problemes?
set /p fix_all="(o)ui / (n)on: "

if /i not "%fix_all%"=="o" (
    echo Installation annulee
    pause
    exit /b 0
)

echo.
echo ====================================
echo   CORRECTION DES PROBLEMES
echo ====================================
echo.

REM Demander le nom du venv si on va le recreer
if not exist "%venv_name%\Scripts\python.exe" (
    echo Nom de l'environnement virtuel?
    set /p custom_venv="[Appuyez sur Entree pour '%venv_name%']: "
    if not "!custom_venv!"=="" set "venv_name=!custom_venv!"
)

REM Recreer l'environnement virtuel si necessaire
if not exist "%venv_name%\Scripts\python.exe" (
    call :create_venv
) else (
    %venv_name%\Scripts\python.exe --version >nul 2>&1
    if errorlevel 1 (
        echo L'environnement virtuel est defectueux, recreation...
        call :create_venv
    )
)

REM Installer les packages si necessaire
if "!packages_ok!"=="0" (
    call :install_packages
)

REM Creer la configuration si necessaire
if defined config_missing (
    call :create_basic_config
)

echo.
echo ====================================
echo   CORRECTION TERMINEE
echo ====================================
echo.

REM Creer les dossiers de travail
if not exist "scan" mkdir scan >nul 2>&1
if not exist "output" mkdir output >nul 2>&1
if not exist "logs" mkdir logs >nul 2>&1

echo Lancement de l'application...
echo.
%venv_name%\Scripts\python.exe gui\ocr_gui.py

:end_with_error_check
if errorlevel 1 (
    echo.
    echo [ERREUR] L'application a rencontre un probleme
    echo.
    echo Solutions possibles:
    echo 1. Supprimez le dossier '%venv_name%' et relancez ce script
    echo 2. Verifiez que Tesseract OCR est installe sur votre systeme
    echo 3. Consultez les logs dans le dossier 'logs'
    pause
)
goto :eof

REM === FONCTIONS ===

:create_venv
echo.
echo Creation de l'environnement virtuel '%venv_name%'...
if exist "%venv_name%" rmdir /s /q "%venv_name%" 2>nul
python -m venv %venv_name%
if errorlevel 1 (
    echo [ERREUR] Impossible de creer l'environnement virtuel
    pause
    exit /b 1
)
echo [OK] Environnement virtuel cree
goto :eof

:install_packages
echo.
echo Installation des packages Python...
%venv_name%\Scripts\python.exe -m pip install --upgrade pip >nul 2>&1

if exist "requirements.txt" (
    echo Installation depuis requirements.txt...
    %venv_name%\Scripts\pip.exe install -r requirements.txt
) else (
    echo Installation des packages essentiels...
    %venv_name%\Scripts\pip.exe install Pillow pdf2image pytesseract opencv-python numpy
)

echo [OK] Packages installes
goto :eof

:create_basic_config
echo.
echo Configuration initiale...
if not exist "src\config" mkdir src\config >nul 2>&1

(echo {
 echo   "scan_folder": "scan",
 echo   "sub_folders": ["Documents"],
 echo   "output_folder": "output"
 echo }) > src\config\config.json

echo [OK] Configuration de base creee
goto :eof
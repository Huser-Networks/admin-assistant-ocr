@echo off
REM OCR Assistant - Script de lancement intelligent
REM Gere automatiquement l'installation et la configuration

chcp 65001 >nul
cd /d "%~dp0"

echo ====================================
echo      OCR ASSISTANT
echo ====================================
echo.

REM Verifier si Python est installe
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe
    echo.
    echo Veuillez installer Python depuis: https://www.python.org/
    echo.
    pause
    exit /b 1
)

REM Detecter les environnements virtuels existants
set "venv_name=ocr-venv"
set "venv_exists=0"
set "venv_works=0"

if exist "%venv_name%\Scripts\python.exe" (
    set "venv_exists=1"
    REM Tester si le venv fonctionne
    %venv_name%\Scripts\python.exe --version >nul 2>&1
    if not errorlevel 1 (
        set "venv_works=1"
    )
)

REM Si le venv n'existe pas ou ne fonctionne pas
if "%venv_works%"=="0" (
    echo [!] Environnement virtuel non trouve ou defectueux
    echo.
    
    if "%venv_exists%"=="1" (
        echo L'environnement virtuel existe mais ne fonctionne pas
        echo (probablement cree avec une autre version de Python)
        echo.
    )
    
    echo Voulez-vous creer un nouvel environnement virtuel?
    set /p create_venv="(o)ui / (n)on / (p)ersonnaliser le nom [o/n/p]: "
    
    if /i "%create_venv%"=="n" (
        echo.
        echo Installation annulee
        pause
        exit /b 0
    )
    
    if /i "%create_venv%"=="p" (
        set /p venv_name="Nom de l'environnement virtuel [ocr-venv]: "
        if "%venv_name%"=="" set "venv_name=ocr-venv"
    )
    
    REM Supprimer l'ancien venv si necessaire
    if exist "%venv_name%" (
        echo.
        echo Suppression de l'ancien environnement...
        rmdir /s /q "%venv_name%" 2>nul
    )
    
    REM Creer le nouvel environnement virtuel
    echo.
    echo Creation de l'environnement virtuel '%venv_name%'...
    python -m venv %venv_name%
    if errorlevel 1 (
        echo [ERREUR] Impossible de creer l'environnement virtuel
        pause
        exit /b 1
    )
    
    echo [OK] Environnement virtuel cree
    echo.
    
    REM Installer les packages
    echo Installation des packages Python...
    echo.
    
    %venv_name%\Scripts\python.exe -m pip install --upgrade pip >nul 2>&1
    
    if exist "requirements.txt" (
        echo Installation depuis requirements.txt...
        %venv_name%\Scripts\pip.exe install -r requirements.txt
    ) else (
        echo Installation des packages essentiels...
        %venv_name%\Scripts\pip.exe install Pillow pdf2image pytesseract opencv-python numpy
    )
    
    REM Tester l'installation
    echo.
    echo Verification de l'installation...
    %venv_name%\Scripts\python.exe -c "import PIL, pdf2image, pytesseract, cv2, numpy; print('[OK] Packages installes')" 2>nul
    if errorlevel 1 (
        echo [ATTENTION] Certains packages peuvent manquer
        echo Continuez quand meme? 
        set /p continue="(o/n): "
        if /i not "!continue!"=="o" (
            pause
            exit /b 1
        )
    )
    echo.
)

REM Verifier si les dossiers necessaires existent
if not exist "scan" mkdir scan
if not exist "output" mkdir output
if not exist "logs" mkdir logs

REM Verifier la configuration
if not exist "src\config\config.json" (
    echo [!] Configuration manquante
    echo Creation de la configuration par defaut...
    
    if not exist "src\config" mkdir src\config
    
    (echo {
     echo   "scan_folder": "scan",
     echo   "sub_folders": ["Documents"],
     echo   "output_folder": "output"
     echo }) > src\config\config.json
    
    echo [OK] Configuration creee
    echo.
)

REM Proposer la configuration si premiere fois
if not exist "src\config\hierarchical_config.json" (
    echo ====================================
    echo   CONFIGURATION INITIALE
    echo ====================================
    echo.
    echo C'est votre premiere utilisation.
    echo Voulez-vous configurer l'application maintenant?
    set /p config_now="(o/n): "
    
    if /i "%config_now%"=="o" (
        echo.
        echo Configuration de base:
        echo ----------------------
        set /p user_name="Votre nom: "
        set /p company="Votre entreprise (optionnel): "
        
        REM Creer la config hierarchique de base
        (echo {
         echo   "global": {
         echo     "user_info": {
         echo       "name": "!user_name!",
         echo       "company": "!company!"
         echo     },
         echo     "ignore_words": []
         echo   },
         echo   "folders": {}
         echo }) > src\config\hierarchical_config.json
        
        echo.
        echo [OK] Configuration sauvegardee
    )
    echo.
)

REM Lancer l'application
echo ====================================
echo   LANCEMENT DE L'APPLICATION
echo ====================================
echo.

REM Determiner le venv a utiliser
if exist "%venv_name%\Scripts\python.exe" (
    echo Lancement avec l'environnement: %venv_name%
    echo.
    %venv_name%\Scripts\python.exe gui\ocr_gui.py
) else (
    echo [ERREUR] Environnement virtuel introuvable
    echo Relancez ce script pour reinstaller
    pause
    exit /b 1
)

if errorlevel 1 (
    echo.
    echo [ERREUR] L'application a rencontre un probleme
    echo.
    echo Solutions possibles:
    echo 1. Supprimez le dossier '%venv_name%' et relancez ce script
    echo 2. Verifiez que Tesseract OCR est installe
    echo 3. Consultez les logs dans le dossier 'logs'
    pause
)
@echo off
REM Script pour recréer l'environnement virtuel avec la bonne version de Python

cd /d "%~dp0"

echo ====================================
echo   RECREATION ENVIRONNEMENT VIRTUEL
echo ====================================
echo.

REM Vérifier la version de Python installée
echo Détection de Python...
python --version
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installé ou pas dans le PATH
    pause
    exit /b 1
)

echo.
echo [ATTENTION] Ceci va supprimer l'ancien environnement virtuel et en créer un nouveau.
echo.
set /p confirm="Continuer ? (o/n): "
if /i not "%confirm%"=="o" (
    echo Annulé.
    pause
    exit /b 0
)

REM Supprimer l'ancien environnement virtuel
if exist "ocr-venv" (
    echo.
    echo Suppression de l'ancien environnement virtuel...
    rmdir /s /q ocr-venv
    if exist "ocr-venv" (
        echo [ERREUR] Impossible de supprimer ocr-venv. Fermez tous les programmes qui l'utilisent.
        pause
        exit /b 1
    )
    echo [OK] Ancien environnement supprimé
)

REM Créer le nouvel environnement virtuel avec Python actuel
echo.
echo Création du nouvel environnement virtuel avec Python actuel...
python -m venv ocr-venv
if errorlevel 1 (
    echo [ERREUR] Impossible de créer l'environnement virtuel
    pause
    exit /b 1
)

echo [OK] Environnement virtuel créé

REM Installer les dépendances
echo.
echo Installation des dépendances...

REM Mise à jour de pip
ocr-venv\Scripts\python.exe -m pip install --upgrade pip

REM Installation des requirements
if exist "requirements.txt" (
    echo Installation depuis requirements.txt...
    ocr-venv\Scripts\pip.exe install -r requirements.txt
) else (
    echo Installation manuelle des packages essentiels...
    ocr-venv\Scripts\pip.exe install Pillow pdf2image pytesseract opencv-python numpy
)

echo.
echo ====================================
echo   ENVIRONNEMENT RECREE AVEC SUCCES
echo ====================================
echo.
echo Vous pouvez maintenant lancer l'application avec:
echo   launch.bat
echo.
pause
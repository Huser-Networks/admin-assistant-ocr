@echo off
REM Lanceur pour OCR Assistant GUI sur Windows
REM Active l'environnement virtuel et lance l'interface

echo ====================================
echo    OCR Assistant - Interface GUI
echo ====================================
echo.

REM Activer l'environnement virtuel
if exist "ocr-venv\Scripts\activate.bat" (
    echo Activation de l'environnement virtuel...
    call ocr-venv\Scripts\activate.bat
) else (
    echo [ERREUR] Environnement virtuel non trouvé!
    echo Veuillez créer l'environnement virtuel avec:
    echo    python -m venv ocr-venv
    echo    ocr-venv\Scripts\activate
    echo    pip install -r requirements.txt
    pause
    exit /b 1
)

REM Vérifier les dépendances
echo Vérification des dépendances...
python -c "from src.utils.dependency_checker import DependencyChecker; exit(0 if DependencyChecker().full_check() else 1)"
if errorlevel 1 (
    echo.
    echo [ATTENTION] Des dépendances sont manquantes.
    echo Installation automatique...
    python -c "from src.utils.dependency_checker import DependencyChecker; DependencyChecker().ensure_dependencies()"
    echo.
)

REM Lancer l'interface graphique
echo Lancement de l'interface...
python ocr_gui.py

REM Si erreur, attendre avant de fermer
if errorlevel 1 (
    echo.
    echo [ERREUR] L'interface n'a pas pu démarrer.
    pause
)
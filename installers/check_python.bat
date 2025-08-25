@echo off
REM Script de diagnostic pour vérifier les versions de Python

echo ====================================
echo   DIAGNOSTIC PYTHON
echo ====================================
echo.

echo === Python système ===
where python
python --version
echo.

echo === Python dans PATH ===
for %%i in (python.exe) do @echo %%~$PATH:i
echo.

echo === Environnement virtuel actuel ===
if exist "ocr-venv\Scripts\python.exe" (
    echo Chemin: ocr-venv\Scripts\python.exe
    ocr-venv\Scripts\python.exe --version 2>nul
    if errorlevel 1 (
        echo [ERREUR] L'environnement virtuel ne fonctionne pas
        echo.
        echo Contenu de ocr-venv\pyvenv.cfg:
        if exist "ocr-venv\pyvenv.cfg" (
            type ocr-venv\pyvenv.cfg
        ) else (
            echo pyvenv.cfg non trouvé
        )
    )
) else (
    echo Environnement virtuel non trouvé
)

echo.
echo === Recommandation ===
echo Si l'environnement virtuel ne fonctionne pas, exécutez:
echo   recreate_venv.bat
echo.
pause
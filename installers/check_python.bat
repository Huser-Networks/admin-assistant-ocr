@echo off
REM Script de diagnostic pour verifier les versions de Python

chcp 65001 >nul
cd /d "%~dp0"
cd ..

echo ====================================
echo   DIAGNOSTIC PYTHON
echo ====================================
echo.

echo === Python systeme ===
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
            echo pyvenv.cfg non trouve
        )
    ) else (
        echo [OK] L'environnement virtuel fonctionne
    )
) else (
    echo Environnement virtuel non trouve
)

echo.
echo === Fichiers et repertoires ===
echo Requirements.txt:
if exist "requirements.txt" (
    echo [OK] requirements.txt existe
) else (
    echo [ERREUR] requirements.txt manquant
)

echo install_dependencies.py:
if exist "installers\install_dependencies.py" (
    echo [OK] script de verification existe
) else (
    echo [ERREUR] script de verification manquant
)

echo.
echo === Recommandation ===
echo Si l'environnement virtuel ne fonctionne pas, executez:
echo   installers\recreate_venv.bat
echo.
pause
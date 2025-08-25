#!/usr/bin/env python3
"""
Lanceur Python pour OCR Assistant
"""
import os
import sys
import subprocess
from pathlib import Path

# Aller au dossier parent (racine du projet)
project_root = Path(__file__).parent.parent
os.chdir(project_root)

# Chemin de l'environnement virtuel
if sys.platform == "win32":
    venv_python = project_root / "ocr-venv" / "Scripts" / "python.exe"
else:
    venv_python = project_root / "ocr-venv" / "bin" / "python"

# Chemin du GUI
gui_path = project_root / "gui" / "ocr_gui.py"

if not venv_python.exists():
    print("Environnement virtuel non trouvé. Exécutez: installers/install_dependencies.py")
    sys.exit(1)

# Lancer le GUI
subprocess.run([str(venv_python), str(gui_path)])
#!/usr/bin/env python3
"""
Lanceur pour OCR Assistant GUI
Compatible Windows, Linux et Mac
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Lance l'interface GUI OCR Assistant"""
    
    print("====================================")
    print("   OCR Assistant - Interface GUI")
    print("====================================")
    print()
    
    # Déterminer le chemin de base
    base_dir = Path(__file__).parent
    
    # Chemins de l'environnement virtuel selon l'OS
    if sys.platform == "win32":
        venv_python = base_dir / "ocr-venv" / "Scripts" / "python.exe"
    else:
        venv_python = base_dir / "ocr-venv" / "bin" / "python"
    
    # Vérifier l'environnement virtuel
    if not venv_python.exists():
        print("[ERREUR] Environnement virtuel non trouvé!")
        print("Veuillez créer l'environnement virtuel avec:")
        print("    python -m venv ocr-venv")
        if sys.platform == "win32":
            print("    ocr-venv\\Scripts\\activate")
        else:
            print("    source ocr-venv/bin/activate")
        print("    pip install -r requirements.txt")
        input("\nAppuyez sur Entrée pour quitter...")
        return 1
    
    # Chemin du GUI
    gui_path = base_dir / "ocr_gui.py"
    
    if not gui_path.exists():
        print("[ERREUR] Fichier ocr_gui.py non trouvé!")
        input("\nAppuyez sur Entrée pour quitter...")
        return 1
    
    # Lancer l'interface
    print("Lancement de l'interface...")
    print(f"Python: {venv_python}")
    print(f"Script: {gui_path}")
    print()
    
    try:
        # Lancer avec l'environnement virtuel
        result = subprocess.run([str(venv_python), str(gui_path)])
        return result.returncode
    except Exception as e:
        print(f"[ERREUR] Impossible de lancer l'interface: {e}")
        input("\nAppuyez sur Entrée pour quitter...")
        return 1

if __name__ == "__main__":
    sys.exit(main())
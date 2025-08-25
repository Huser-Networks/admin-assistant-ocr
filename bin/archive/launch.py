#!/usr/bin/env python3
"""
Lanceur principal pour OCR Assistant
Utilise toujours l'environnement virtuel ocr-venv
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Lance l'interface GUI OCR Assistant avec le bon environnement"""
    
    print("====================================")
    print("   OCR Assistant - Lancement")
    print("====================================")
    print()
    
    # Déterminer le chemin de base
    base_dir = Path(__file__).parent.resolve()
    os.chdir(base_dir)
    
    # Chemins de l'environnement virtuel selon l'OS
    if sys.platform == "win32":
        venv_python = base_dir / "ocr-venv" / "Scripts" / "python.exe"
    else:
        venv_python = base_dir / "ocr-venv" / "bin" / "python"
    
    # Vérifier l'environnement virtuel
    if not venv_python.exists():
        print("[ERREUR] Environnement virtuel non trouvé!")
        print("\nCréez d'abord l'environnement avec:")
        print("    python -m venv ocr-venv")
        print("    ocr-venv\\Scripts\\activate  (Windows)")
        print("    source ocr-venv/bin/activate  (Linux/Mac)")
        print("    pip install -r requirements.txt")
        print("\nOu exécutez: python installers/install_dependencies.py")
        input("\nAppuyez sur Entrée pour quitter...")
        return 1
    
    # Chemin du GUI
    gui_path = base_dir / "gui" / "ocr_gui.py"
    
    if not gui_path.exists():
        print(f"[ERREUR] Fichier GUI non trouvé: {gui_path}")
        input("\nAppuyez sur Entrée pour quitter...")
        return 1
    
    print(f"Environnement: {venv_python}")
    print(f"Script GUI: {gui_path}")
    print("\nLancement de l'interface...")
    print()
    
    try:
        # Lancer avec l'environnement virtuel
        result = subprocess.run([str(venv_python), str(gui_path)], cwd=str(base_dir))
        return result.returncode
    except Exception as e:
        print(f"[ERREUR] Impossible de lancer l'interface: {e}")
        input("\nAppuyez sur Entrée pour quitter...")
        return 1

if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
Crée un raccourci bureau pour OCR Assistant sur Windows
"""

import os
import sys
from pathlib import Path

def create_windows_shortcut():
    """Crée un raccourci Windows sur le bureau"""
    
    try:
        import winshell
        from win32com.client import Dispatch
    except ImportError:
        print("Installation des dépendances Windows...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32", "winshell"])
        import winshell
        from win32com.client import Dispatch
    
    # Chemins
    desktop = winshell.desktop()
    base_dir = Path(__file__).parent.resolve()
    
    # Créer le raccourci
    shell = Dispatch('WScript.Shell')
    shortcut_path = os.path.join(desktop, "OCR Assistant.lnk")
    shortcut = shell.CreateShortCut(shortcut_path)
    
    # Configurer le raccourci
    shortcut.Targetpath = str(base_dir / "launch_gui.bat")
    shortcut.WorkingDirectory = str(base_dir)
    shortcut.IconLocation = "pythonw.exe"
    shortcut.Description = "OCR Assistant - Traitement automatique de PDFs"
    
    # Sauvegarder
    shortcut.save()
    
    print(f"✅ Raccourci créé sur le bureau: {shortcut_path}")
    return shortcut_path

def main():
    """Point d'entrée principal"""
    
    print("====================================")
    print("  Création du Raccourci Bureau")
    print("====================================")
    print()
    
    if sys.platform != "win32":
        print("Ce script est uniquement pour Windows.")
        print("Sur Linux/Mac, ajoutez un alias dans votre shell:")
        print(f"    alias ocr-assistant='python {Path(__file__).parent / 'launch_gui.py'}'")
        return 1
    
    try:
        shortcut_path = create_windows_shortcut()
        print()
        print("Le raccourci a été créé avec succès!")
        print("Vous pouvez maintenant lancer OCR Assistant depuis votre bureau.")
        input("\nAppuyez sur Entrée pour quitter...")
        return 0
    except Exception as e:
        print(f"[ERREUR] Impossible de créer le raccourci: {e}")
        input("\nAppuyez sur Entrée pour quitter...")
        return 1

if __name__ == "__main__":
    sys.exit(main())
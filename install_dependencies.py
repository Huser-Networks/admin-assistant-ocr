#!/usr/bin/env python3
"""
Script d'installation des dépendances pour OCR Assistant
"""

import sys
import os

# Ajouter le chemin pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.dependency_checker import DependencyChecker

def main():
    """Point d'entrée principal"""
    
    print("="*60)
    print("   INSTALLATION DES DÉPENDANCES OCR ASSISTANT")
    print("="*60)
    print()
    
    checker = DependencyChecker()
    
    # Vérifier et installer les packages Python
    print("📦 Installation des packages Python...")
    if checker.ensure_dependencies():
        print("✅ Packages Python installés")
    else:
        print("❌ Échec de l'installation des packages Python")
        return 1
    
    print()
    
    # Vérifier Tesseract
    print("🔍 Vérification de Tesseract OCR...")
    if not checker.check_tesseract():
        print("\n⚠️ IMPORTANT: Tesseract OCR doit être installé séparément")
        print("Téléchargez-le depuis: https://github.com/UB-Mannheim/tesseract/wiki")
        print("Ou utilisez Chocolatey sur Windows: choco install tesseract")
    
    print()
    
    # Vérifier Poppler (Windows)
    import platform
    if platform.system() == "Windows":
        print("🔍 Vérification de Poppler...")
        if not checker.check_poppler():
            print("\n⚠️ IMPORTANT: Poppler doit être installé pour Windows")
            print("1. Téléchargez depuis: https://github.com/oschwartz10612/poppler-windows/releases")
            print("2. Extrayez dans C:\\Tools\\poppler")
            print("3. Ajoutez C:\\Tools\\poppler\\Library\\bin au PATH")
    
    print("\n" + "="*60)
    print("Installation terminée!")
    print("Lancez l'interface avec: python launch_gui.py")
    print("="*60)
    
    input("\nAppuyez sur Entrée pour quitter...")
    return 0

if __name__ == "__main__":
    sys.exit(main())
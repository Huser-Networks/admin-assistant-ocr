#!/usr/bin/env python3
"""
Vérificateur et installateur de dépendances
"""

import sys
import subprocess
import importlib.util
from typing import List, Tuple

class DependencyChecker:
    """Vérifie et installe les dépendances manquantes"""
    
    REQUIRED_PACKAGES = {
        'PIL': 'Pillow',
        'pdf2image': 'pdf2image',
        'pytesseract': 'pytesseract',
        'cv2': 'opencv-python',
        'numpy': 'numpy'
    }
    
    @staticmethod
    def check_package(import_name: str) -> bool:
        """Vérifie si un package est installé"""
        spec = importlib.util.find_spec(import_name)
        return spec is not None
    
    @classmethod
    def check_all_packages(cls) -> Tuple[List[str], List[str]]:
        """
        Vérifie tous les packages requis
        Retourne (packages_installés, packages_manquants)
        """
        installed = []
        missing = []
        
        for import_name, pip_name in cls.REQUIRED_PACKAGES.items():
            if cls.check_package(import_name):
                installed.append(pip_name)
            else:
                missing.append(pip_name)
        
        return installed, missing
    
    @staticmethod
    def install_package(package_name: str) -> bool:
        """Installe un package via pip"""
        try:
            print(f"📦 Installation de {package_name}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package_name
            ])
            print(f"✅ {package_name} installé avec succès")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'installation de {package_name}: {e}")
            return False
    
    @classmethod
    def install_missing_packages(cls, missing_packages: List[str]) -> bool:
        """Installe tous les packages manquants"""
        if not missing_packages:
            return True
        
        print("\n" + "="*50)
        print("📋 Packages manquants détectés:")
        for pkg in missing_packages:
            print(f"   - {pkg}")
        print("="*50 + "\n")
        
        success = True
        for package in missing_packages:
            if not cls.install_package(package):
                success = False
        
        return success
    
    @classmethod
    def ensure_dependencies(cls) -> bool:
        """
        Vérifie et installe automatiquement les dépendances manquantes
        Retourne True si tout est OK, False sinon
        """
        print("🔍 Vérification des dépendances...")
        installed, missing = cls.check_all_packages()
        
        if not missing:
            print("✅ Toutes les dépendances sont installées")
            return True
        
        print(f"⚠️ {len(missing)} dépendance(s) manquante(s)")
        
        # Installer les packages manquants
        if cls.install_missing_packages(missing):
            print("\n✅ Toutes les dépendances ont été installées avec succès")
            return True
        else:
            print("\n❌ Certaines dépendances n'ont pas pu être installées")
            print("Veuillez les installer manuellement avec:")
            print(f"   pip install {' '.join(missing)}")
            return False
    
    @staticmethod
    def check_tesseract() -> bool:
        """Vérifie si Tesseract OCR est installé sur le système"""
        import platform
        
        if platform.system() == "Windows":
            # Chemins Windows
            paths = [
                r'C:\Tools\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
            ]
            
            import os
            for path in paths:
                if os.path.exists(path):
                    return True
            
            print("⚠️ Tesseract OCR non trouvé")
            print("Veuillez l'installer depuis: https://github.com/UB-Mannheim/tesseract/wiki")
            print("Ou via Chocolatey: choco install tesseract")
            return False
        else:
            # Linux/Mac - vérifier via which
            try:
                subprocess.run(["which", "tesseract"], 
                             check=True, capture_output=True)
                return True
            except subprocess.CalledProcessError:
                print("⚠️ Tesseract OCR non trouvé")
                print("Installation:")
                print("  Ubuntu/Debian: sudo apt-get install tesseract-ocr")
                print("  Mac: brew install tesseract")
                return False
    
    @staticmethod
    def check_poppler() -> bool:
        """Vérifie si Poppler est installé (nécessaire pour pdf2image)"""
        import platform
        
        if platform.system() == "Windows":
            # Chemins Windows pour Poppler
            paths = [
                r'C:\Tools\poppler\Library\bin',
                r'C:\Program Files\poppler\bin',
                r'C:\Program Files (x86)\poppler\bin'
            ]
            
            import os
            for path in paths:
                if os.path.exists(path):
                    # Ajouter au PATH si nécessaire
                    if path not in os.environ.get('PATH', ''):
                        os.environ['PATH'] = path + os.pathsep + os.environ.get('PATH', '')
                    return True
            
            print("⚠️ Poppler non trouvé")
            print("Veuillez le télécharger depuis: https://github.com/oschwartz10612/poppler-windows/releases")
            print("Et l'extraire dans C:\\Tools\\poppler")
            return False
        else:
            # Linux/Mac - généralement installé avec pdf2image
            return True
    
    @classmethod
    def full_check(cls) -> bool:
        """
        Effectue une vérification complète de l'environnement
        """
        print("\n" + "="*60)
        print("🔧 VÉRIFICATION COMPLÈTE DE L'ENVIRONNEMENT")
        print("="*60 + "\n")
        
        all_ok = True
        
        # 1. Vérifier les packages Python
        if not cls.ensure_dependencies():
            all_ok = False
        
        print()
        
        # 2. Vérifier Tesseract
        print("🔍 Vérification de Tesseract OCR...")
        if cls.check_tesseract():
            print("✅ Tesseract OCR est installé")
        else:
            all_ok = False
        
        print()
        
        # 3. Vérifier Poppler (Windows)
        import platform
        if platform.system() == "Windows":
            print("🔍 Vérification de Poppler...")
            if cls.check_poppler():
                print("✅ Poppler est installé")
            else:
                all_ok = False
        
        print("\n" + "="*60)
        if all_ok:
            print("✅ ENVIRONNEMENT PRÊT - Tout est correctement installé!")
        else:
            print("⚠️ CONFIGURATION INCOMPLÈTE - Veuillez installer les composants manquants")
        print("="*60 + "\n")
        
        return all_ok


if __name__ == "__main__":
    # Test du vérificateur
    checker = DependencyChecker()
    if checker.full_check():
        print("L'application est prête à être utilisée!")
        sys.exit(0)
    else:
        print("Veuillez corriger les problèmes ci-dessus avant de continuer.")
        sys.exit(1)
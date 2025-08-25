#!/usr/bin/env python3
"""
Configuration hiérarchique avec héritage et surcharges
"""

import os
import sys
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils.hierarchical_config import HierarchicalConfig


class HierarchicalConfigurator:
    """Interface de configuration hiérarchique"""
    
    def __init__(self):
        self.config_manager = HierarchicalConfig()
        self.config = self.config_manager.config
    
    def run(self):
        """Lance la configuration interactive"""
        
        print("🎯 CONFIGURATION HIÉRARCHIQUE OCR ASSISTANT")
        print("="*50)
        print("Système d'héritage: Global → Dossiers spécifiques")
        print("Chaque dossier peut AJOUTER (+) ou RETIRER (-) des éléments\n")
        
        # 1. Configuration globale
        self.configure_global()
        
        # 2. Créer les dossiers
        folders = self.create_folders()
        
        # 3. Configurer chaque dossier
        self.configure_folders(folders)
        
        # 4. Résumé
        self.show_summary()
    
    def configure_global(self):
        """Configure les informations globales"""
        
        print("🌍 CONFIGURATION GLOBALE")
        print("="*30)
        print("Ces informations seront IGNORÉES dans TOUS les dossiers")
        print("(sauf si explicitement ajoutées avec + dans un dossier)\n")
        
        # Noms à ignorer globalement
        print("👤 Vos noms/prénoms (Entrée pour terminer):")
        names = []
        while True:
            name = input(f"  Nom {len(names)+1}: ").strip()
            if not name:
                break
            names.append(name)
        
        # Adresses à ignorer
        print("\n🏠 Vos adresses (Entrée pour terminer):")
        addresses = []
        while True:
            addr = input(f"  Adresse {len(addresses)+1}: ").strip()
            if not addr:
                break
            addresses.append(addr)
        
        # Entreprises par défaut (si applicable)
        print("\n🏢 Vos entreprises par défaut (Entrée pour terminer):")
        companies = []
        while True:
            company = input(f"  Entreprise {len(companies)+1}: ").strip()
            if not company:
                break
            companies.append(company)
        
        # Mettre à jour la config globale
        global_info = {
            "user_info": {
                "names": names,
                "addresses": addresses,
                "companies": companies
            }
        }
        
        self.config_manager.update_global_config(user_info=global_info["user_info"])
        
        print(f"\n✅ Configuration globale enregistrée:")
        print(f"   - {len(names)} nom(s)")
        print(f"   - {len(addresses)} adresse(s)")
        print(f"   - {len(companies)} entreprise(s)")
    
    def detect_existing_folders(self):
        """Détecte les dossiers existants dans scan/"""
        existing = []
        scan_path = "scan"
        
        if os.path.exists(scan_path):
            for item in os.listdir(scan_path):
                item_path = os.path.join(scan_path, item)
                if os.path.isdir(item_path):
                    existing.append(item)
        
        return existing
    
    def create_folders(self):
        """Crée ou détecte les dossiers de tri"""
        
        print("\n📂 GESTION DES DOSSIERS DE TRI")
        print("="*35)
        
        # Détecter les dossiers existants
        existing_folders = self.detect_existing_folders()
        
        if existing_folders:
            print(f"📁 Dossiers existants détectés: {', '.join(existing_folders)}")
            print("\nOptions:")
            print("1. Utiliser les dossiers existants")
            print("2. Ajouter des nouveaux dossiers")
            print("3. Repartir de zéro")
            
            choice = input("\nVotre choix (1/2/3): ").strip()
            
            if choice == "1":
                folders = existing_folders
                print(f"✅ Utilisation des {len(folders)} dossiers existants")
            elif choice == "2":
                folders = existing_folders.copy()
                print("\n📝 Ajoutez des dossiers supplémentaires (Entrée pour terminer):")
                
                while True:
                    folder = input(f"  Nouveau dossier {len(folders)+1}: ").strip()
                    if not folder:
                        break
                    
                    folder_clean = folder.replace(" ", "").replace("/", "").replace("\\", "")
                    
                    if folder_clean not in folders:
                        folders.append(folder_clean)
                        os.makedirs(f"scan/{folder_clean}", exist_ok=True)
                        os.makedirs(f"output/{folder_clean}", exist_ok=True)
                        print(f"    ✅ Ajouté: {folder_clean}")
                    else:
                        print(f"    ⚠️  '{folder_clean}' existe déjà")
            else:
                # Repartir de zéro
                folders = self.create_new_folders()
        else:
            print("Aucun dossier existant détecté.\n")
            folders = self.create_new_folders()
        
        # Sauvegarder dans config.json principal
        config_main = {
            "scan_folder": "scan",
            "sub_folders": folders,
            "output_folder": "output"
        }
        
        os.makedirs("src/config", exist_ok=True)
        with open("src/config/config.json", 'w', encoding='utf-8') as f:
            json.dump(config_main, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ {len(folders)} dossier(s) configuré(s)")
        return folders
    
    def create_new_folders(self):
        """Crée de nouveaux dossiers"""
        folders = []
        
        print("\n📝 Noms des dossiers (Entrée pour terminer):")
        print("Exemples: Personnel, EntrepriseSARL, FacturesEDF, DocsPourAmi\n")
        
        while True:
            folder = input(f"  Dossier {len(folders)+1}: ").strip()
            
            if not folder:
                if len(folders) == 0:
                    print("  ⚠️  Au moins un dossier nécessaire!")
                    continue
                break
            
            # Nettoyer le nom
            folder_clean = folder.replace(" ", "").replace("/", "").replace("\\", "")
            
            if folder_clean not in folders:
                folders.append(folder_clean)
                
                # Créer la structure physique
                os.makedirs(f"scan/{folder_clean}", exist_ok=True)
                os.makedirs(f"output/{folder_clean}", exist_ok=True)
                
                print(f"    ✅ Créé: {folder_clean}")
        
        return folders
    
    def configure_folders(self, folders):
        """Configure chaque dossier individuellement"""
        
        print("\n⚙️  CONFIGURATION PAR DOSSIER")
        print("="*35)
        print("Pour chaque dossier, définissez les AJOUTS (+) et SUPPRESSIONS (-)")
        print("par rapport à la configuration globale\n")
        
        for folder in folders:
            print(f"\n📁 Configuration pour: {folder}")
            print("-" * 30)
            
            # Demander le type de configuration
            print("\nOptions:")
            print("1. Utiliser uniquement la config globale")
            print("2. Personnaliser (ajouter/retirer des éléments)")
            
            choice = input("\nVotre choix (1/2): ").strip()
            
            if choice == "2":
                add_config = {}
                remove_config = {}
                
                # AJOUTS
                print(f"\n➕ AJOUTS pour {folder}:")
                
                # Ajouter des noms ?
                add_names = input("  Ajouter des noms spécifiques ? (o/n): ").lower()
                if add_names == 'o':
                    names = []
                    print("  Noms à AJOUTER (Entrée pour terminer):")
                    while True:
                        name = input(f"    +Nom: ").strip()
                        if not name:
                            break
                        names.append(name)
                    if names:
                        add_config.setdefault('user_info', {})['names'] = names
                
                # Ajouter des entreprises ?
                add_companies = input("  Ajouter des entreprises ? (o/n): ").lower()
                if add_companies == 'o':
                    companies = []
                    print("  Entreprises à AJOUTER:")
                    while True:
                        company = input(f"    +Entreprise: ").strip()
                        if not company:
                            break
                        companies.append(company)
                    if companies:
                        add_config.setdefault('user_info', {})['companies'] = companies
                
                # Ajouter des adresses ?
                add_addresses = input("  Ajouter des adresses ? (o/n): ").lower()
                if add_addresses == 'o':
                    addresses = []
                    print("  Adresses à AJOUTER:")
                    while True:
                        addr = input(f"    +Adresse: ").strip()
                        if not addr:
                            break
                        addresses.append(addr)
                    if addresses:
                        add_config.setdefault('user_info', {})['addresses'] = addresses
                
                # SUPPRESSIONS
                print(f"\n➖ SUPPRESSIONS pour {folder}:")
                
                # Retirer des noms globaux ?
                if self.config['global']['user_info']['names']:
                    print(f"  Noms globaux: {', '.join(self.config['global']['user_info']['names'][:3])}")
                    remove_names = input("  Retirer certains noms globaux ? (o/n): ").lower()
                    if remove_names == 'o':
                        names = []
                        print("  Noms à RETIRER (parmi les globaux):")
                        for name in self.config['global']['user_info']['names']:
                            keep = input(f"    Garder '{name}' ? (o/n): ").lower()
                            if keep == 'n':
                                names.append(name)
                        if names:
                            remove_config.setdefault('user_info', {})['names'] = names
                
                # Description du dossier
                desc = input(f"\n📝 Description pour {folder} (optionnel): ").strip()
                
                # Sauvegarder la config du dossier
                self.config_manager.add_folder_config(
                    folder, 
                    description=desc,
                    add_config=add_config,
                    remove_config=remove_config
                )
                
                print(f"✅ Configuration de {folder} enregistrée")
            else:
                # Utiliser config globale uniquement
                self.config_manager.add_folder_config(folder, description="Config globale uniquement")
                print(f"✅ {folder} utilisera la config globale")
    
    def show_summary(self):
        """Affiche un résumé de la configuration"""
        
        print("\n📊 RÉSUMÉ DE LA CONFIGURATION")
        print("="*40)
        
        # Config globale
        global_cfg = self.config.get('global', {})
        user_info = global_cfg.get('user_info', {})
        
        print("\n🌍 GLOBAL (ignoré partout sauf exception):")
        print(f"  - Noms: {', '.join(user_info.get('names', [])[:3])}")
        print(f"  - Adresses: {', '.join(user_info.get('addresses', [])[:2])}")
        print(f"  - Entreprises: {', '.join(user_info.get('companies', [])[:2])}")
        
        # Configs par dossier
        print("\n📁 PAR DOSSIER:")
        for folder_name, folder_cfg in self.config.get('folders', {}).items():
            print(f"\n  {folder_name}:")
            
            # Récupérer la config effective
            effective = self.config_manager.get_folder_config(folder_name)
            
            if folder_cfg.get('add'):
                print(f"    ➕ Ajouts: {self._format_changes(folder_cfg['add'])}")
            if folder_cfg.get('remove'):
                print(f"    ➖ Retraits: {self._format_changes(folder_cfg['remove'])}")
            
            # Résultat effectif
            eff_info = effective.get('user_info', {})
            print(f"    📋 Résultat: {len(eff_info.get('names', []))} noms, "
                  f"{len(eff_info.get('addresses', []))} adresses, "
                  f"{len(eff_info.get('companies', []))} entreprises")
        
        print("\n✅ Configuration terminée!")
        print("📖 Fichier: src/config/hierarchical_config.json")
        print("🚀 Lancez: run_windows.bat")
    
    def _format_changes(self, changes):
        """Formate les changements pour l'affichage"""
        parts = []
        if 'user_info' in changes:
            info = changes['user_info']
            if 'names' in info:
                parts.append(f"{len(info['names'])} nom(s)")
            if 'companies' in info:
                parts.append(f"{len(info['companies'])} entreprise(s)")
            if 'addresses' in info:
                parts.append(f"{len(info['addresses'])} adresse(s)")
        return ", ".join(parts) if parts else "aucun"


def main():
    configurator = HierarchicalConfigurator()
    configurator.run()


if __name__ == "__main__":
    main()
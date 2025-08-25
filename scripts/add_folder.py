#!/usr/bin/env python3
"""
Script pour ajouter rapidement un nouveau dossier à la configuration existante
"""

import os
import json
import sys

def load_current_config():
    """Charge la configuration actuelle"""
    config_file = "src/config/config.json"
    
    if not os.path.exists(config_file):
        print("❌ Configuration non trouvée. Lancez d'abord: python scripts/setup_user_config.py")
        sys.exit(1)
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    return config

def add_new_folder():
    """Ajoute un nouveau dossier à la configuration"""
    
    print("➕ AJOUT D'UN NOUVEAU DOSSIER")
    print("="*30)
    
    # Charger config actuelle
    config = load_current_config()
    current_folders = config.get('sub_folders', [])
    
    print(f"📁 Dossiers actuels: {', '.join(current_folders)}")
    print()
    
    # Demander le nouveau dossier
    while True:
        folder_name = input("📝 Nom du nouveau dossier: ").strip()
        
        if not folder_name:
            print("⚠️  Le nom ne peut pas être vide !")
            continue
        
        # Nettoyer le nom
        folder_clean = folder_name.replace(" ", "").replace("/", "").replace("\\", "")
        
        if folder_clean in current_folders:
            print(f"⚠️  '{folder_clean}' existe déjà !")
            continue
        
        break
    
    # Créer la structure de dossiers
    scan_folder = f"scan/{folder_clean}"
    output_folder = f"output/{folder_clean}"
    
    os.makedirs(scan_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)
    
    print(f"\n✅ Dossiers créés:")
    print(f"  - {scan_folder}")
    print(f"  - {output_folder}")
    
    # Mettre à jour la configuration
    current_folders.append(folder_clean)
    config['sub_folders'] = current_folders
    
    with open("src/config/config.json", 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Configuration mise à jour")
    
    # Demander si on veut créer un profil
    create_profile = input(f"\n📋 Créer un profil pour '{folder_clean}' ? (o/n): ").lower()
    
    if create_profile == 'o':
        create_folder_profile(folder_clean)
    else:
        print(f"\n💡 Vous pouvez créer le profil plus tard dans:")
        print(f"   src/config/profiles/{folder_clean}.json")
    
    print(f"\n🎉 Dossier '{folder_clean}' ajouté avec succès !")
    print(f"📄 Placez vos PDFs dans: {scan_folder}")
    print(f"🚀 Lancez le traitement: run_windows.bat")

def create_folder_profile(folder_name):
    """Crée un profil pour le nouveau dossier"""
    
    print(f"\n📋 CRÉATION DU PROFIL POUR '{folder_name}'")
    print("-" * 30)
    
    # Options simples ou détaillées
    print("\n🔧 Options:")
    print("1. Copier le profil global")
    print("2. Configuration personnalisée")
    
    choice = input("\nVotre choix (1/2): ").strip()
    
    if choice == "1":
        # Copier le profil global
        profile = {
            "profile_name": folder_name,
            "inherits_from": "global",
            "user_info": {},
            "supplier_mappings": {}
        }
    else:
        # Configuration personnalisée
        print("\n👤 Configuration personnalisée:")
        
        # Collecte simplifiée
        names = []
        print("\n📝 Vos noms (Entrée pour terminer):")
        while True:
            name = input(f"  Nom {len(names)+1}: ").strip()
            if not name:
                break
            names.append(name)
        
        addresses = []
        print("\n🏠 Vos adresses (Entrée pour terminer):")
        while True:
            address = input(f"  Adresse {len(addresses)+1}: ").strip()
            if not address:
                break
            addresses.append(address)
        
        # Fournisseurs rapides
        suppliers = {}
        print("\n🏪 Fournisseurs principaux (Entrée pour terminer):")
        print("Format: Nom complet = Nom court (ex: Électricité de France = Edf)")
        
        while True:
            entry = input("  Fournisseur: ").strip()
            if not entry:
                break
            
            if "=" in entry:
                full_name, short_name = entry.split("=", 1)
                suppliers[full_name.strip()] = short_name.strip()
            else:
                suppliers[entry] = entry.split()[0]  # Premier mot par défaut
        
        profile = {
            "profile_name": folder_name,
            "inherits_from": "global",
            "user_info": {
                "names": names,
                "addresses": addresses
            },
            "supplier_mappings": suppliers
        }
    
    # Sauvegarder le profil
    os.makedirs("src/config/profiles", exist_ok=True)
    profile_file = f"src/config/profiles/{folder_name}.json"
    
    with open(profile_file, 'w', encoding='utf-8') as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Profil créé: {profile_file}")

def main():
    """Point d'entrée principal"""
    
    print("🚀 AJOUT DE DOSSIER - OCR ASSISTANT")
    print("="*40)
    print("Ajouter un nouveau dossier à votre configuration")
    print()
    
    add_new_folder()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Script interactif pour configurer rapidement l'OCR Assistant
"""

import os
import json
import sys

def create_directory_structure(sub_folders):
    """Crée la structure de dossiers selon les choix utilisateur"""
    
    print("\n📁 Création de la structure de dossiers...")
    
    # Dossiers de base toujours créés
    base_folders = ["output", "logs"]
    for folder in base_folders:
        os.makedirs(folder, exist_ok=True)
        print(f"  ✅ {folder}")
    
    # Créer les sous-dossiers scan selon les choix
    for folder in sub_folders:
        scan_folder = f"scan/{folder}"
        output_folder = f"output/{folder}"
        os.makedirs(scan_folder, exist_ok=True)
        os.makedirs(output_folder, exist_ok=True)
        print(f"  ✅ {scan_folder}")
        print(f"  ✅ {output_folder}")
    
    print()

def collect_user_info():
    """Collecte les informations utilisateur"""
    
    print("👤 CONFIGURATION DE VOTRE PROFIL")
    print("="*40)
    print("Ces informations permettront d'éviter que votre adresse")
    print("soit détectée comme fournisseur dans les documents.\n")
    
    # Noms
    print("📝 Noms (appuyez sur Entrée pour terminer):")
    names = []
    while True:
        name = input(f"  Nom {len(names)+1}: ").strip()
        if not name:
            break
        names.append(name)
    
    # Adresses
    print("\n🏠 Adresses (appuyez sur Entrée pour terminer):")
    addresses = []
    while True:
        address = input(f"  Adresse {len(addresses)+1}: ").strip()
        if not address:
            break
        addresses.append(address)
    
    # Entreprises
    print("\n🏢 Entreprises/Sociétés (si applicable):")
    companies = []
    while True:
        company = input(f"  Société {len(companies)+1}: ").strip()
        if not company:
            break
        companies.append(company)
    
    # Email et téléphone (optionnel)
    email = input("\n📧 Email principal (optionnel): ").strip()
    phone = input("📞 Téléphone principal (optionnel): ").strip()
    
    user_info = {
        "names": names,
        "addresses": addresses,
        "companies": companies
    }
    
    if email:
        user_info["emails"] = [email]
    if phone:
        user_info["phones"] = [phone]
    
    return user_info

def collect_suppliers():
    """Collecte les fournisseurs habituels"""
    
    print("\n🏪 FOURNISSEURS HABITUELS")
    print("="*30)
    print("Listez vos fournisseurs principaux pour améliorer la détection.\n")
    
    categories = {
        "Énergie": ["EDF", "Engie", "Total", "Veolia"],
        "Télécom": ["Orange", "Free", "SFR", "Bouygues"],
        "Banques": ["Crédit Agricole", "BNP", "Société Générale", "LCL"],
        "Commerce": ["Amazon", "Fnac", "Carrefour", "Auchan"]
    }
    
    suppliers = {}
    
    for category, examples in categories.items():
        print(f"\n📂 {category} (exemples: {', '.join(examples[:2])}, ...):")
        category_suppliers = []
        
        while True:
            supplier = input(f"  Fournisseur: ").strip()
            if not supplier:
                break
            
            # Demander le nom court
            short_name = input(f"  Nom court pour '{supplier}': ").strip()
            if not short_name:
                short_name = supplier.split()[0]  # Premier mot par défaut
            
            suppliers[supplier] = short_name
            category_suppliers.append(f"{supplier} → {short_name}")
        
        if category_suppliers:
            print(f"  ✅ Ajoutés: {', '.join(category_suppliers)}")
    
    return suppliers

def create_main_config(sub_folders):
    """Crée la configuration principale"""
    
    config = {
        "scan_folder": "scan",
        "sub_folders": sub_folders,
        "output_folder": "output"
    }
    
    with open("src/config/config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Configuration principale créée avec {len(sub_folders)} dossiers")

def create_user_profile(profile_name, user_info, suppliers):
    """Crée un profil utilisateur"""
    
    profile = {
        "profile_name": profile_name,
        "inherits_from": "global",
        "user_info": user_info,
        "supplier_mappings": suppliers,
        "naming_rules": {
            "format": "{date}_{supplier}_{invoice}",
            "use_camel_case": True,
            "max_filename_length": 100
        }
    }
    
    # Créer le dossier profiles s'il n'existe pas
    os.makedirs("src/config/profiles", exist_ok=True)
    
    # Sauvegarder le profil
    profile_file = f"src/config/profiles/{profile_name}.json"
    with open(profile_file, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2, ensure_ascii=False)
    
    return profile_file

def collect_folders():
    """Collecte les dossiers souhaités par l'utilisateur"""
    
    print("📂 CONFIGURATION DES DOSSIERS")
    print("="*30)
    print("Créez les dossiers pour organiser vos documents.")
    print("Exemples: Personnel, Factures, Medical, Banque, Entreprise1, etc.\n")
    
    folders = []
    
    # Suggestions par défaut
    print("💡 Suggestions courantes:")
    print("  - Personnel (documents personnels)")
    print("  - Factures (toutes vos factures)")
    print("  - Medical (documents médicaux)")
    print("  - Banque (relevés bancaires)")
    print("  - Entreprise (documents professionnels)")
    print("  - Impots (documents fiscaux)")
    print()
    
    print("📝 Ajoutez vos dossiers (appuyez sur Entrée pour terminer):")
    print("Conseil: Utilisez des noms courts et sans espaces (ex: FacturesEDF)\n")
    
    while True:
        folder_name = input(f"  Dossier {len(folders)+1}: ").strip()
        
        if not folder_name:
            if len(folders) == 0:
                print("  ⚠️  Au moins un dossier est nécessaire !")
                continue
            else:
                break
        
        # Nettoyer le nom (enlever espaces, caractères spéciaux)
        folder_clean = folder_name.replace(" ", "").replace("/", "").replace("\\", "")
        
        if folder_clean and folder_clean not in folders:
            folders.append(folder_clean)
            print(f"    ✅ Ajouté: {folder_clean}")
        elif folder_clean in folders:
            print(f"    ⚠️  '{folder_clean}' existe déjà")
    
    print(f"\n✅ {len(folders)} dossier(s) configuré(s): {', '.join(folders)}")
    return folders

def main():
    """Configuration interactive"""
    
    print("🚀 CONFIGURATION INTERACTIVE OCR ASSISTANT")
    print("="*50)
    print("Ce script va vous aider à configurer rapidement")
    print("l'OCR Assistant selon vos besoins.\n")
    
    # Collecte des dossiers souhaités
    selected_folders = collect_folders()
    
    # Créer la structure
    create_directory_structure(selected_folders)
    
    # Configuration principale
    create_main_config(selected_folders)
    
    # Informations utilisateur
    user_info = collect_user_info()
    
    # Fournisseurs
    suppliers = collect_suppliers()
    
    # Créer les profils pour chaque dossier sélectionné
    print(f"\n💾 CRÉATION DES PROFILS")
    print("="*25)
    
    # Demander si on veut le même profil pour tous ou personnalisé
    if len(selected_folders) > 1:
        print("\n🔧 Options de configuration:")
        print("1. Utiliser la même configuration pour tous les dossiers")
        print("2. Personnaliser chaque dossier séparément")
        choice = input("\nVotre choix (1/2): ").strip()
        
        if choice == "2":
            # Configuration personnalisée par dossier
            created_profiles = []
            for folder in selected_folders:
                print(f"\n📁 Configuration pour '{folder}':")
                print("-" * 30)
                
                # Demander si on veut des infos spécifiques
                custom = input("  Voulez-vous des paramètres spécifiques ? (o/n): ").lower()
                
                if custom == 'o':
                    print(f"\n  Configuration spécifique pour {folder}:")
                    folder_user_info = collect_user_info()
                    folder_suppliers = collect_suppliers()
                else:
                    folder_user_info = user_info
                    folder_suppliers = suppliers
                
                profile_file = create_user_profile(folder, folder_user_info, folder_suppliers)
                created_profiles.append(profile_file)
                print(f"  ✅ Profil créé: {profile_file}")
        else:
            # Même config pour tous
            created_profiles = []
            for folder in selected_folders:
                profile_file = create_user_profile(folder, user_info, suppliers)
                created_profiles.append(profile_file)
                print(f"  ✅ Profil créé: {profile_file}")
    else:
        # Un seul dossier
        created_profiles = []
        for folder in selected_folders:
            profile_file = create_user_profile(folder, user_info, suppliers)
            created_profiles.append(profile_file)
            print(f"  ✅ Profil créé: {profile_file}")
    
    # Résumé final
    print(f"\n🎉 CONFIGURATION TERMINÉE !")
    print("="*30)
    print(f"📁 Dossiers configurés: {', '.join(selected_folders)}")
    print(f"👤 Informations utilisateur: {len(user_info['names'])} nom(s), {len(user_info['addresses'])} adresse(s)")
    print(f"🏪 Fournisseurs mappés: {len(suppliers)}")
    print(f"📋 Profils créés: {len(created_profiles)}")
    
    print(f"\n🚀 PROCHAINES ÉTAPES:")
    print("1. Placez vos PDFs dans les dossiers scan/")
    print("2. Lancez: run_windows.bat")
    print("3. Révisez les résultats: python scripts/review_results.py")
    print("\n📖 Guide complet: docs/MANUEL_UTILISATEUR.md")

if __name__ == "__main__":
    main()
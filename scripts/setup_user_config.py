#!/usr/bin/env python3
"""
Script interactif pour configurer rapidement l'OCR Assistant
"""

import os
import json
import sys

def create_directory_structure():
    """Crée la structure de dossiers recommandée"""
    
    folders = [
        "scan/Personnel",
        "scan/Entreprise", 
        "scan/Medical",
        "scan/Banque",
        "scan/Factures",
        "output",
        "logs"
    ]
    
    print("📁 Création de la structure de dossiers...")
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"  ✅ {folder}")
    
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

def main():
    """Configuration interactive"""
    
    print("🚀 CONFIGURATION INTERACTIVE OCR ASSISTANT")
    print("="*50)
    print("Ce script va vous aider à configurer rapidement")
    print("l'OCR Assistant selon vos besoins.\n")
    
    # Créer la structure
    create_directory_structure()
    
    # Dossiers à utiliser
    print("📂 CHOIX DES DOSSIERS")
    print("="*25)
    print("Quels types de documents voulez-vous traiter ?")
    
    available_folders = ["Personnel", "Entreprise", "Medical", "Banque", "Factures"]
    selected_folders = []
    
    for folder in available_folders:
        choice = input(f"  Utiliser '{folder}' ? (o/n): ").lower()
        if choice == 'o':
            selected_folders.append(folder)
    
    if not selected_folders:
        selected_folders = ["Personnel"]  # Au moins un dossier
        print("  ⚠️  Aucun dossier sélectionné, utilisation de 'Personnel' par défaut")
    
    # Configuration principale
    create_main_config(selected_folders)
    
    # Informations utilisateur
    user_info = collect_user_info()
    
    # Fournisseurs
    suppliers = collect_suppliers()
    
    # Créer les profils pour chaque dossier sélectionné
    print(f"\n💾 CRÉATION DES PROFILS")
    print("="*25)
    
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
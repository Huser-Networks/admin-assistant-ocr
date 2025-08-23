#!/usr/bin/env python3
"""
Script pour réviser et corriger les résultats d'extraction OCR
"""

import sys
import os
import json
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.learning_system import LearningSystem
from src.utils.logger import Logger


class ReviewInterface:
    """Interface pour réviser les extractions"""
    
    def __init__(self):
        self.logger = Logger()
        self.learning_system = LearningSystem()
        self.results_file = 'logs/last_extraction_results.json'
    
    def save_extraction_for_review(self, file_path, ocr_text, extracted_data, final_filename):
        """Sauvegarde une extraction pour révision ultérieure"""
        result = {
            'timestamp': str(Path(file_path).stat().st_mtime),
            'original_file': file_path,
            'final_filename': final_filename,
            'extracted_data': extracted_data,
            'ocr_text_preview': ocr_text[:500] + "..." if len(ocr_text) > 500 else ocr_text
        }
        
        # Charger les résultats existants
        results = []
        if os.path.exists(self.results_file):
            try:
                with open(self.results_file, 'r', encoding='utf-8') as f:
                    results = json.load(f)
            except:
                results = []
        
        results.append(result)
        
        # Garder seulement les 50 derniers
        results = results[-50:]
        
        # Sauvegarder
        os.makedirs(os.path.dirname(self.results_file), exist_ok=True)
        with open(self.results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
    
    def review_last_results(self):
        """Interface pour réviser les derniers résultats"""
        
        if not os.path.exists(self.results_file):
            print("❌ Aucun résultat à réviser. Lancez d'abord le traitement OCR.")
            return
        
        with open(self.results_file, 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        if not results:
            print("❌ Aucun résultat trouvé.")
            return
        
        print(f"📋 {len(results)} résultat(s) à réviser\n")
        
        for i, result in enumerate(results[-10:], 1):  # 10 derniers
            self.review_single_result(i, result)
    
    def review_single_result(self, index, result):
        """Révise un résultat individuel"""
        
        print(f"{'='*60}")
        print(f"📄 RÉSULTAT {index}")
        print(f"{'='*60}")
        print(f"📁 Fichier original: {result['original_file']}")
        print(f"📁 Nom généré: {result['final_filename']}")
        print()
        
        extracted = result['extracted_data']
        print("🔍 EXTRACTIONS:")
        print(f"📅 Date: {extracted.get('date', 'NON TROUVÉE')}")
        print(f"🏢 Fournisseur: {extracted.get('supplier', 'NON TROUVÉ')}")
        print(f"📋 Numéro: {extracted.get('invoice', 'NON TROUVÉ')}")
        print()
        
        print("📄 APERÇU DU TEXTE OCR:")
        print(result['ocr_text_preview'])
        print()
        
        # Demander validation
        response = input("✅ Cette extraction est-elle correcte ? (o/n/s pour skip): ").lower()
        
        if response == 'n':
            self.collect_corrections(result)
        elif response == 's':
            print("⏭️ Ignoré\n")
        else:
            print("✅ Validé\n")
            # Enregistrer comme succès
            self.learning_system.record_extraction(
                result['original_file'],
                result.get('ocr_text_preview', ''),
                extracted,
                result['final_filename']
            )
    
    def collect_corrections(self, result):
        """Collecte les corrections de l'utilisateur"""
        
        extracted = result['extracted_data']
        ocr_text = result.get('ocr_text_preview', '')
        
        print("\n🔧 CORRECTION NÉCESSAIRE")
        print("Laissez vide pour garder la valeur actuelle\n")
        
        # Correction de la date
        current_date = extracted.get('date', '')
        print(f"📅 Date actuelle: {current_date}")
        new_date = input("📅 Nouvelle date (YYYYMMDD): ").strip()
        if new_date and new_date != current_date:
            self.learning_system.add_correction(
                'date_corrections', ocr_text, new_date, current_date
            )
            print(f"✅ Date corrigée: {new_date}")
        
        # Correction du fournisseur
        current_supplier = extracted.get('supplier', '')
        print(f"\n🏢 Fournisseur actuel: {current_supplier}")
        new_supplier = input("🏢 Nouveau fournisseur: ").strip()
        if new_supplier and new_supplier != current_supplier:
            self.learning_system.add_correction(
                'supplier_corrections', ocr_text, new_supplier, current_supplier
            )
            print(f"✅ Fournisseur corrigé: {new_supplier}")
        
        # Correction du numéro
        current_invoice = extracted.get('invoice', '')
        print(f"\n📋 Numéro actuel: {current_invoice}")
        new_invoice = input("📋 Nouveau numéro: ").strip()
        if new_invoice and new_invoice != current_invoice:
            self.learning_system.add_correction(
                'invoice_corrections', ocr_text, new_invoice, current_invoice
            )
            print(f"✅ Numéro corrigé: {new_invoice}")
        
        print("\n✅ Corrections enregistrées ! Le système s'améliorera.\n")
    
    def show_learning_stats(self):
        """Affiche les statistiques d'apprentissage"""
        
        report = self.learning_system.generate_improvement_report()
        print(report)
        
        # Afficher les corrections apprises
        corrections = self.learning_system.corrections
        total_corrections = sum(len(corr) for corr in corrections.values())
        
        print(f"\n🧠 APPRENTISSAGE ACTUEL:")
        print(f"📚 Total corrections apprises: {total_corrections}")
        
        for corr_type, corr_data in corrections.items():
            if corr_data:
                type_name = corr_type.replace('_corrections', '')
                print(f"  - {type_name.capitalize()}: {len(corr_data)} corrections")


def main():
    """Menu principal"""
    
    interface = ReviewInterface()
    
    while True:
        print("\n" + "="*50)
        print("🧠 SYSTÈME DE RÉVISION ET APPRENTISSAGE")
        print("="*50)
        print("1. Réviser les derniers résultats")
        print("2. Voir les statistiques d'apprentissage") 
        print("3. Quitter")
        print()
        
        choice = input("Votre choix (1-3): ").strip()
        
        if choice == '1':
            interface.review_last_results()
        elif choice == '2':
            interface.show_learning_stats()
        elif choice == '3':
            print("👋 Au revoir !")
            break
        else:
            print("❌ Choix invalide")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Script de test pour valider et améliorer la configuration OCR
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.document_analyzer import DocumentAnalyzer
from src.extractors.date_extractor import DateExtractor
from src.extractors.supplier_extractor import SupplierExtractor
from src.extractors.invoice_extractor import InvoiceExtractor


def test_extraction_with_sample(ocr_text, document_name="Test"):
    """Test l'extraction sur un échantillon de texte OCR"""
    
    print(f"\n{'='*60}")
    print(f"TEST: {document_name}")
    print(f"{'='*60}")
    
    print("📄 TEXTE OCR (premiers 200 caractères):")
    print(ocr_text[:200] + "..." if len(ocr_text) > 200 else ocr_text)
    print()
    
    # Test des extracteurs
    date_extractor = DateExtractor()
    supplier_extractor = SupplierExtractor()
    invoice_extractor = InvoiceExtractor()
    
    # Extraction
    date = date_extractor.extract(ocr_text)
    supplier = supplier_extractor.extract(ocr_text)
    invoice_num = invoice_extractor.extract(ocr_text)
    
    # Résultats
    print("🔍 RÉSULTATS D'EXTRACTION:")
    print(f"📅 Date: {date or 'NON TROUVÉE'}")
    print(f"🏢 Fournisseur: {supplier or 'NON TROUVÉ'}")
    print(f"📋 Numéro: {invoice_num or 'NON TROUVÉ'}")
    
    # Nom de fichier final
    filename = DocumentAnalyzer.generate_filename(ocr_text, f"{document_name}.pdf")
    print(f"📁 Nom de fichier: {filename}")
    
    return {
        'date': date,
        'supplier': supplier, 
        'invoice': invoice_num,
        'filename': filename
    }


def main():
    """Fonction principale de test"""
    
    print("🧪 TESTEUR DE CONFIGURATION OCR")
    print("Permet de tester l'extraction sur des échantillons de texte")
    
    # Échantillons de test
    samples = {
        "Facture EDF": """
EDF
Électricité de France
Société Anonyme au capital de 1 551 810 543 euros
22-30 Avenue de Wagram - 75382 Paris cedex 08
552 081 317 RCS Paris

FACTURE D'ELECTRICITE

Destinataire:
M. Jean DUPONT
123 rue de la République
75001 PARIS

Facture n° : FAC-2024-001234
Date de facture : 15 mars 2024
Période du 15/02/2024 au 14/03/2024

Montant à payer : 89,50 €
Date d'échéance : 15 avril 2024
""",
        
        "Document Hôpital": """
HÔPITAL NECKER - ENFANTS MALADES
149 rue de Sèvres
75015 PARIS
Tél : 01 44 49 40 00

COMPTE-RENDU DE CONSULTATION

Patient : Jean DUPONT
N° de dossier : PAT123456
Date de naissance : 15/06/1985

Consultation du 22 janvier 2024
Service de cardiologie
Dr. Martin DURAND

Destinataire:
M. Jean DUPONT  
123 rue de la République
75001 PARIS

Référence : CR-CARDIO-20240122-001
""",
        
        "Facture Orange": """
Orange
Société Anonyme
78 rue Olivier de Serres
75015 Paris

FACTURE MOBILE

Période du 01/02/2024 au 29/02/2024
Date de facture: 01/03/2024

Client:
M. Jean DUPONT
123 rue de la République  
75001 PARIS
N° Client: CLI987654321

Référence facture: ORA-2024-FEB-789456
Montant: 45,99 €
Échéance: 25/03/2024
"""
    }
    
    # Tester chaque échantillon
    results = {}
    for name, text in samples.items():
        results[name] = test_extraction_with_sample(text, name)
    
    # Résumé
    print(f"\n{'='*60}")
    print("📊 RÉSUMÉ DES TESTS")
    print(f"{'='*60}")
    
    for name, result in results.items():
        print(f"\n{name}:")
        print(f"  ✅ Date: {result['date'] is not None}")
        print(f"  ✅ Fournisseur: {result['supplier'] != 'Fournisseur_Inconnu'}")
        print(f"  ✅ Numéro: {result['invoice'] is not None}")
        print(f"  📁 {result['filename']}")
    
    print(f"\n{'='*60}")
    print("💡 POUR AMÉLIORER:")
    print("1. Ajoutez vos infos dans src/config/profiles/[dossier].json")
    print("2. Testez avec vos vrais PDFs")
    print("3. Ajustez les patterns dans extraction_rules.json")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
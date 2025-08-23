#!/usr/bin/env python3
"""
Test pour vérifier le format des noms de fichiers générés
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.document_analyzer import DocumentAnalyzer


def test_filename_generation():
    """Test de génération des noms de fichiers"""
    
    print("🧪 TEST DU FORMAT DE NOMMAGE")
    print("="*50)
    
    # Cas de test
    test_cases = [
        {
            'text': '''
EDF Électricité de France
Facture n° FAC-2024-001
Date: 15/03/2024
Destinataire: M. Jean DUPONT
            ''',
            'expected_pattern': '20240315_Edf_FAC2024001.pdf'
        },
        {
            'text': '''
CAISSE D'EPARGNE ILE DE FRANCE
Relevé de compte
Période du 01/02/2024 au 29/02/2024
Référence: BDC45678
            ''',
            'expected_pattern': '20240229_CaisseDEpargne_BDC45678.pdf'
        },
        {
            'text': '''
Orange Mobile
Facture du 01/03/2024
Référence client: ORA-2024-789
            ''',
            'expected_pattern': '20240301_OrangeMobile_ORA2024789.pdf'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📄 TEST {i}:")
        print("Texte OCR:", test_case['text'].strip()[:100] + "...")
        
        # Générer le nom de fichier
        generated = DocumentAnalyzer.generate_filename(test_case['text'])
        
        print(f"🎯 Attendu (pattern): {test_case['expected_pattern']}")
        print(f"📁 Généré: {generated}")
        
        # Vérifier le format général
        parts = generated.replace('.pdf', '').split('_')
        
        if len(parts) >= 2:
            date_part = parts[0]
            if len(date_part) == 8 and date_part.isdigit():
                print("✅ Format date OK (YYYYMMDD)")
            else:
                print("❌ Format date incorrect")
            
            if len(parts) >= 3:
                supplier_part = parts[1]
                number_part = parts[2]
                print(f"✅ Format complet: Date_{supplier_part}_{number_part}.pdf")
            elif len(parts) == 2:
                supplier_part = parts[1]
                print(f"⚠️  Format partiel: Date_{supplier_part}.pdf (pas de numéro)")
        else:
            print("❌ Format incorrect")
        
        print("-" * 30)
    
    print("\n💡 FORMAT ATTENDU:")
    print("📋 Complet: YYYYMMDD_FournisseurCamelCase_NumeroReference.pdf")
    print("📋 Partiel: YYYYMMDD_FournisseurCamelCase.pdf")
    print("📋 Minimal: YYYYMMDD_Document.pdf")


if __name__ == "__main__":
    test_filename_generation()
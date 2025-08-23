import json
import os
from datetime import datetime
from src.utils.logger import Logger


class LearningSystem:
    """Système d'apprentissage pour améliorer l'extraction"""
    
    def __init__(self):
        self.logger = Logger()
        self.corrections_file = 'src/config/corrections.json'
        self.stats_file = 'src/config/extraction_stats.json'
        self.corrections = self.load_corrections()
        self.stats = self.load_stats()
    
    def load_corrections(self):
        """Charge les corrections précédentes"""
        try:
            if os.path.exists(self.corrections_file):
                with open(self.corrections_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"Erreur chargement corrections: {e}")
        
        return {
            'date_corrections': {},
            'supplier_corrections': {},
            'invoice_corrections': {},
            'filename_corrections': {}
        }
    
    def load_stats(self):
        """Charge les statistiques d'extraction"""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"Erreur chargement stats: {e}")
        
        return {
            'total_processed': 0,
            'successful_extractions': {
                'date': 0,
                'supplier': 0,
                'invoice': 0
            },
            'common_suppliers': {},
            'common_patterns': {},
            'error_patterns': []
        }
    
    def record_extraction(self, file_path, ocr_text, extracted_data, final_filename):
        """Enregistre une extraction pour les statistiques"""
        
        # Mettre à jour les stats
        self.stats['total_processed'] += 1
        
        if extracted_data.get('date'):
            self.stats['successful_extractions']['date'] += 1
        
        if extracted_data.get('supplier'):
            self.stats['successful_extractions']['supplier'] += 1
            supplier = extracted_data['supplier']
            self.stats['common_suppliers'][supplier] = self.stats['common_suppliers'].get(supplier, 0) + 1
        
        if extracted_data.get('invoice'):
            self.stats['successful_extractions']['invoice'] += 1
        
        # Sauvegarder
        self.save_stats()
        
        self.logger.debug(f"Extraction enregistrée: {final_filename}")
    
    def suggest_correction(self, original_filename, extracted_data, ocr_text):
        """Propose des corrections basées sur l'historique"""
        suggestions = {}
        
        # Chercher des patterns similaires dans les corrections
        for correction_type, corrections in self.corrections.items():
            for pattern, correction_data in corrections.items():
                if self.is_similar_pattern(ocr_text, pattern):
                    suggestions[correction_type] = correction_data
                    break
        
        return suggestions
    
    def is_similar_pattern(self, text1, text2, threshold=0.7):
        """Compare la similarité entre deux textes (méthode simple)"""
        words1 = set(text1.lower().split()[:20])  # Premiers 20 mots
        words2 = set(text2.lower().split()[:20])
        
        if not words1 or not words2:
            return False
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        similarity = len(intersection) / len(union)
        return similarity >= threshold
    
    def add_correction(self, correction_type, original_text, corrected_value, original_extraction):
        """Ajoute une correction manuelle"""
        
        if correction_type not in self.corrections:
            self.corrections[correction_type] = {}
        
        # Utiliser les premiers mots comme clé pattern
        pattern_key = ' '.join(original_text.split()[:20])
        
        correction_data = {
            'corrected_value': corrected_value,
            'original_extraction': original_extraction,
            'timestamp': datetime.now().isoformat(),
            'confidence': 'manual_correction'
        }
        
        self.corrections[correction_type][pattern_key] = correction_data
        self.save_corrections()
        
        self.logger.info(f"Correction ajoutée pour {correction_type}: {corrected_value}")
    
    def get_learned_patterns(self, extraction_type):
        """Retourne les patterns appris pour un type d'extraction"""
        patterns = []
        
        corrections = self.corrections.get(f"{extraction_type}_corrections", {})
        for pattern, data in corrections.items():
            patterns.append({
                'pattern': pattern,
                'value': data['corrected_value'],
                'confidence': 'learned'
            })
        
        return patterns
    
    def generate_improvement_report(self):
        """Génère un rapport d'amélioration"""
        total = self.stats['total_processed']
        if total == 0:
            return "Aucun document traité encore."
        
        successful = self.stats['successful_extractions']
        
        report = f"""
=== RAPPORT D'AMÉLIORATION OCR ===

📊 STATISTIQUES GLOBALES:
- Documents traités: {total}
- Taux de succès date: {(successful['date']/total)*100:.1f}%
- Taux de succès fournisseur: {(successful['supplier']/total)*100:.1f}%  
- Taux de succès numéro: {(successful['invoice']/total)*100:.1f}%

🏢 FOURNISSEURS LES PLUS FRÉQUENTS:
"""
        
        # Top 5 fournisseurs
        top_suppliers = sorted(
            self.stats['common_suppliers'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        for supplier, count in top_suppliers:
            report += f"- {supplier}: {count} documents\n"
        
        report += f"\n🔧 CORRECTIONS APPRISES: {len(self.corrections.get('date_corrections', {}))}\n"
        
        # Suggestions d'amélioration
        report += "\n💡 RECOMMANDATIONS:\n"
        
        if successful['date']/total < 0.8:
            report += "- Améliorer la détection de dates (ajouter des patterns)\n"
        
        if successful['supplier']/total < 0.7:
            report += "- Affiner l'extraction du fournisseur (revoir user_info)\n"
        
        if successful['invoice']/total < 0.6:
            report += "- Améliorer la détection des numéros de référence\n"
        
        return report
    
    def save_corrections(self):
        """Sauvegarde les corrections"""
        try:
            os.makedirs(os.path.dirname(self.corrections_file), exist_ok=True)
            with open(self.corrections_file, 'w', encoding='utf-8') as f:
                json.dump(self.corrections, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde corrections: {e}")
    
    def save_stats(self):
        """Sauvegarde les statistiques"""
        try:
            os.makedirs(os.path.dirname(self.stats_file), exist_ok=True)
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde stats: {e}")
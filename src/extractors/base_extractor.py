from abc import ABC, abstractmethod
import json
import os
from src.utils.logger import Logger


class BaseExtractor(ABC):
    """Classe de base pour tous les extracteurs de métadonnées"""
    
    def __init__(self):
        self.logger = Logger()
        self.rules = self.load_rules()
    
    def load_rules(self):
        """Charge les règles de configuration"""
        rules_path = 'src/config/extraction_rules.json'
        try:
            with open(rules_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Erreur chargement règles: {e}")
            return {}
    
    @abstractmethod
    def extract(self, text):
        """Méthode à implémenter par chaque extracteur"""
        pass
    
    def get_confidence_score(self, text, extracted_value, context_keywords):
        """Calcule un score de confiance pour une valeur extraite"""
        if not extracted_value:
            return 0
        
        score = 50  # Score de base
        text_lower = text.lower()
        
        # Bonus si proche de mots-clés contextuels
        for keyword in context_keywords:
            if keyword in text_lower:
                # Distance entre le mot-clé et la valeur
                keyword_pos = text_lower.find(keyword)
                value_pos = text_lower.find(extracted_value.lower())
                if keyword_pos != -1 and value_pos != -1:
                    distance = abs(keyword_pos - value_pos)
                    if distance < 100:
                        score += (100 - distance) / 5
        
        return min(100, score)  # Plafonner à 100
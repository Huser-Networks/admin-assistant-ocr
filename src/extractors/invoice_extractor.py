import re
from src.extractors.base_extractor import BaseExtractor


class InvoiceExtractor(BaseExtractor):
    """Extracteur pour les numéros de facture et références"""
    
    def extract(self, text):
        """Extrait le numéro de facture ou référence le plus probable"""
        text_lower = text.lower()
        candidates = []
        
        # Parcourir les différents types de patterns
        for pattern_type, config in self.rules.get('invoice_patterns', {}).items():
            keywords = config.get('keywords', [])
            patterns = config.get('patterns', [])
            max_length = config.get('max_length', 30)
            
            for keyword in keywords:
                # Chercher le mot-clé dans le texte
                pos = text_lower.find(keyword)
                if pos != -1:
                    # Extraire le contexte après le mot-clé
                    context_start = pos + len(keyword)
                    context = text[context_start:context_start + 100]
                    
                    # Appliquer les patterns
                    for pattern in patterns:
                        match = re.search(pattern, context, re.IGNORECASE)
                        if match:
                            value = match.group(1).strip()
                            
                            # Nettoyer et valider
                            value = self.clean_invoice_number(value, max_length)
                            
                            if value and self.is_valid_invoice_number(value):
                                score = self.calculate_invoice_score(
                                    value, keyword, pattern_type, pos
                                )
                                
                                candidates.append({
                                    'number': value,
                                    'score': score,
                                    'type': pattern_type,
                                    'keyword': keyword
                                })
        
        # Retourner le meilleur candidat
        if candidates:
            candidates.sort(key=lambda x: x['score'], reverse=True)
            best = candidates[0]
            self.logger.info(f"Numéro extrait: {best['number']} (type: {best['type']}, score: {best['score']:.1f})")
            return best['number']
        
        self.logger.debug("Aucun numéro trouvé")
        return None
    
    def clean_invoice_number(self, value, max_length):
        """Nettoie le numéro de facture"""
        # Enlever les espaces en trop
        value = value.strip()
        
        # Enlever les caractères non désirés à la fin
        value = re.sub(r'[\s\.,;:]+$', '', value)
        
        # Limiter la longueur
        if len(value) > max_length:
            value = value[:max_length]
        
        # Remplacer les espaces par des underscores
        value = re.sub(r'\s+', '_', value)
        
        return value
    
    def is_valid_invoice_number(self, value):
        """Vérifie si c'est un numéro valide"""
        # Doit contenir au moins un chiffre
        if not re.search(r'\d', value):
            return False
        
        # Ne doit pas être juste un nombre de téléphone
        if re.match(r'^0\d{9}$', value):
            return False
        
        # Ne doit pas être une date
        if re.match(r'^\d{2}/\d{2}/\d{4}$', value):
            return False
        
        # Longueur minimale
        if len(value) < 2:
            return False
        
        return True
    
    def calculate_invoice_score(self, value, keyword, pattern_type, position):
        """Calcule le score d'un numéro trouvé"""
        score = 50  # Score de base
        
        # Bonus selon le type
        type_scores = {
            'standard': 30,
            'reference': 25,
            'order': 20,
            'quote': 15
        }
        score += type_scores.get(pattern_type, 10)
        
        # Bonus si contient un préfixe standard
        if re.match(r'^(FAC|INV|REF|CMD|BC|DEV)', value, re.IGNORECASE):
            score += 20
        
        # Bonus si proche du début
        if position < 300:
            score += 15
        
        # Bonus si format structuré (lettres et chiffres)
        if re.match(r'^[A-Z]+[-/]?\d+', value, re.IGNORECASE):
            score += 15
        
        return score
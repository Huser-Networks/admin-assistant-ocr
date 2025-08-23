import re
from datetime import datetime
from src.extractors.base_extractor import BaseExtractor


class DateExtractor(BaseExtractor):
    """Extracteur spécialisé pour les dates"""
    
    MONTHS = {
        'janvier': '01', 'février': '02', 'mars': '03', 'avril': '04',
        'mai': '05', 'juin': '06', 'juillet': '07', 'août': '08',
        'septembre': '09', 'octobre': '10', 'novembre': '11', 'décembre': '12',
        'jan': '01', 'fév': '02', 'mar': '03', 'avr': '04',
        'jun': '06', 'juil': '07', 'aoû': '08', 'sep': '09',
        'oct': '10', 'nov': '11', 'déc': '12'
    }
    
    def extract(self, text):
        """Extrait la date la plus probable du document"""
        text_lower = text.lower()
        candidates = []
        
        # Parcourir tous les types de patterns configurés
        for pattern_type, config in self.rules.get('date_patterns', {}).items():
            patterns = config.get('patterns', [])
            keywords = config.get('keywords', [])
            priority = config.get('priority', 5)
            
            for pattern in patterns:
                matches = re.finditer(pattern, text_lower)
                for match in matches:
                    # Calculer le score
                    score = self.calculate_date_score(
                        text_lower, match, keywords, priority
                    )
                    
                    # Parser la date
                    parsed_date = self.parse_date(match, pattern_type)
                    if parsed_date:
                        candidates.append({
                            'date': parsed_date,
                            'score': score,
                            'type': pattern_type,
                            'original': match.group()
                        })
        
        if not candidates:
            self.logger.debug("Aucune date trouvée")
            return None
        
        # Trier par score et retourner la meilleure
        candidates.sort(key=lambda x: x['score'], reverse=True)
        best = candidates[0]
        
        self.logger.info(f"Date extraite: {best['date']} (score: {best['score']:.1f}, type: {best['type']})")
        return best['date']
    
    def calculate_date_score(self, text, match, keywords, base_priority):
        """Calcule le score d'une date trouvée"""
        position = match.start()
        score = base_priority * 10
        
        # Bonus pour proximité avec mots-clés
        for keyword in keywords:
            # Chercher en arrière (max 50 caractères)
            search_start = max(0, position - 50)
            keyword_pos = text.rfind(keyword, search_start, position)
            if keyword_pos != -1:
                distance = position - keyword_pos
                score += (50 - distance) * 2
        
        # Pénalité si trop loin du début
        if position > 500:
            score -= (position - 500) / 100
        
        return score
    
    def parse_date(self, match, pattern_type):
        """Parse une date selon son type"""
        try:
            groups = match.groups()
            
            if pattern_type == 'french_text':
                # Format avec mois en texte
                day = groups[0].zfill(2)
                month = self.MONTHS.get(groups[1], None)
                if not month:
                    return None
                year = groups[2]
                return f"{year}{month}{day}"
            
            elif pattern_type == 'iso':
                # Format ISO YYYY-MM-DD
                year = groups[0]
                month = groups[1].zfill(2)
                day = groups[2].zfill(2)
                return f"{year}{month}{day}"
            
            else:
                # Format DD/MM/YYYY par défaut
                day = groups[0].zfill(2)
                month = groups[1].zfill(2)
                year = groups[2]
                
                # Validation basique
                if int(month) > 12 or int(day) > 31:
                    return None
                    
                return f"{year}{month}{day}"
                
        except Exception as e:
            self.logger.debug(f"Erreur parsing date: {e}")
            return None
    
    def extract_with_type(self, text, document_type=None):
        """Extraction avec prise en compte du type de document"""
        # Si on connaît le type de document, on peut adapter la recherche
        if document_type and document_type in self.rules.get('document_types', {}):
            doc_config = self.rules['document_types'][document_type]
            # Ajouter des mots-clés spécifiques au type
            specific_keywords = doc_config.get('identifiers', [])
            # TODO: Utiliser ces mots-clés pour améliorer la détection
        
        return self.extract(text)
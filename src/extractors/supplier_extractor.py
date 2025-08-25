import re
import json
import unicodedata
from src.extractors.base_extractor import BaseExtractor


class SupplierExtractor(BaseExtractor):
    """Extracteur intelligent pour identifier le fournisseur en évitant le destinataire"""
    
    def __init__(self, folder_name=None):
        super().__init__()
        self.folder_name = folder_name
        
        # Utiliser la config hiérarchique
        from src.utils.hierarchical_config import HierarchicalConfig
        self.config_manager = HierarchicalConfig()
        
        # Charger la config pour ce dossier spécifique
        if folder_name:
            self.user_profile = self.config_manager.get_folder_config(folder_name)
        else:
            # Fallback sur l'ancienne méthode
            self.user_profile = self.load_user_profile()
    
    def load_user_profile(self):
        """Charge le profil utilisateur pour filtrer les infos personnelles (fallback)"""
        try:
            with open('src/config/user_profile.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.warning(f"Profil utilisateur non trouvé: {e}")
            return {'user_info': {}, 'extraction_zones': {}}
    
    def extract(self, text):
        """Extrait le nom du fournisseur en évitant le destinataire"""
        lines = text.split('\n')
        candidates = []
        
        # Identifier les zones à éviter (destinataire)
        recipient_zones = self.identify_recipient_zones(lines)
        
        # Parcourir les lignes en évitant les zones de destinataire
        for i, line in enumerate(lines[:30]):  # Focus sur le début du document
            line = line.strip()
            
            # Ignorer les lignes vides ou trop courtes
            if len(line) < 3:
                continue
            
            # Vérifier si on est dans une zone destinataire
            if self.is_in_recipient_zone(i, recipient_zones):
                self.logger.debug(f"Ligne {i} ignorée (zone destinataire): {line[:50]}")
                continue
            
            # Vérifier si la ligne contient des infos utilisateur
            if self.contains_user_info(line):
                self.logger.debug(f"Ligne {i} ignorée (info utilisateur): {line[:50]}")
                continue
            
            # Calculer le score de cette ligne
            score = self.calculate_supplier_score(line, i, lines)
            
            if score > 0:
                candidates.append({
                    'name': self.clean_supplier_name(line),
                    'score': score,
                    'line_number': i,
                    'original': line
                })
        
        # Retourner le meilleur candidat
        if candidates:
            candidates.sort(key=lambda x: x['score'], reverse=True)
            best = candidates[0]
            self.logger.info(f"Fournisseur extrait: {best['name']} (score: {best['score']:.1f})")
            return best['name']
        
        self.logger.warning("Aucun fournisseur identifié")
        return "Fournisseur_Inconnu"
    
    def identify_recipient_zones(self, lines):
        """Identifie les zones contenant l'adresse du destinataire"""
        zones = []
        recipient_keywords = self.user_profile.get('extraction_zones', {}).get('recipient_zone', {}).get('keywords', [])
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            for keyword in recipient_keywords:
                if keyword in line_lower:
                    # Marquer une zone de 5 lignes après ce mot-clé
                    zones.append((i, i + 5))
                    self.logger.debug(f"Zone destinataire détectée ligne {i}: {keyword}")
                    break
        
        # Fusionner les zones qui se chevauchent
        merged_zones = []
        for start, end in sorted(zones):
            if merged_zones and start <= merged_zones[-1][1]:
                merged_zones[-1] = (merged_zones[-1][0], max(end, merged_zones[-1][1]))
            else:
                merged_zones.append((start, end))
        
        return merged_zones
    
    def is_in_recipient_zone(self, line_number, zones):
        """Vérifie si une ligne est dans une zone destinataire"""
        for start, end in zones:
            if start <= line_number <= end:
                return True
        return False
    
    def contains_user_info(self, line):
        """
        Vérifie si la ligne contient des informations de l'utilisateur
        selon la configuration hiérarchique du dossier
        """
        if self.folder_name and hasattr(self.config_manager, 'is_user_info'):
            # Utiliser la nouvelle méthode hiérarchique
            return self.config_manager.is_user_info(line, self.folder_name)
        
        # Fallback sur l'ancienne méthode
        line_lower = line.lower()
        user_info = self.user_profile.get('user_info', {})
        
        # Vérifier les noms
        for name in user_info.get('names', []):
            if name.lower() in line_lower:
                self.logger.debug(f"Nom utilisateur trouvé: {name}")
                return True
        
        # Vérifier les adresses
        for address in user_info.get('addresses', []):
            if address.lower() in line_lower:
                self.logger.debug(f"Adresse utilisateur trouvée: {address}")
                return True
        
        # Vérifier les sociétés de l'utilisateur
        for company in user_info.get('companies', []):
            if company.lower() in line_lower:
                self.logger.debug(f"Entreprise utilisateur trouvée: {company}")
                return True
        
        return False
    
    def calculate_supplier_score(self, line, line_number, all_lines):
        """Calcule le score pour identifier si c'est le fournisseur"""
        score = 0
        line_lower = line.lower()
        
        # Bonus si en début de document
        if line_number < 10:
            score += 20 - line_number * 2
        
        # Bonus pour indicateurs d'entreprise
        company_indicators = self.rules.get('supplier_rules', {}).get('company_indicators', [])
        for indicator in company_indicators:
            if indicator in line_lower:
                score += 30
                break
        
        # Bonus si avant les mots-clés de facture
        prefer_keywords = self.user_profile.get('extraction_zones', {}).get('supplier_zone', {}).get('prefer_before_keywords', [])
        for keyword in prefer_keywords:
            # Chercher le mot-clé dans les lignes suivantes
            for j in range(line_number + 1, min(line_number + 10, len(all_lines))):
                if keyword in all_lines[j].lower():
                    score += 15
                    break
        
        # Pénalité pour mots-clés négatifs
        avoid_keywords = self.user_profile.get('extraction_zones', {}).get('supplier_zone', {}).get('avoid_after_keywords', [])
        for keyword in avoid_keywords:
            if keyword in line_lower:
                score -= 50
        
        # Vérifier la longueur et le format
        if 5 < len(line) < 60:
            score += 10
        
        # Pénalité si ressemble à une adresse (contient des chiffres au début)
        if re.match(r'^\d+\s+', line):
            score -= 20
        
        return max(0, score)
    
    def clean_supplier_name(self, text):
        """Nettoie le nom du fournisseur"""
        # Enlever les mentions légales mais garder le nom
        text = re.sub(r'\b(siren|siret|tva|n°tva|rcs|ape|naf|capital).*', '', text, flags=re.IGNORECASE)
        
        # Garder le nom mais enlever le type de société à la fin
        text = re.sub(r'\s+(sarl|sas|sa|eurl|sasu|eirl|sàrl)(\s|$)', '', text, flags=re.IGNORECASE)
        
        # Enlever les caractères spéciaux excessifs
        text = re.sub(r'[•▪►]', '', text)
        
        # Limiter la longueur
        text = text.strip()[:50]
        
        return text if text else "Fournisseur"
    
    def to_camel_case(self, text):
        """Convertit en CamelCase pour le nom de fichier"""
        # Enlever les accents
        text = self.remove_accents(text)
        # Diviser par espaces et caractères spéciaux
        words = re.split(r'[\s\-_,\.]+', text)
        # Capitaliser et joindre
        return ''.join(word.capitalize() for word in words if word)
    
    def remove_accents(self, text):
        """Enlève les accents pour le nom de fichier"""
        nfd = unicodedata.normalize('NFD', text)
        without_accents = ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')
        return without_accents
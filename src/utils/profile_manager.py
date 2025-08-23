import json
import os
from src.utils.logger import Logger


class ProfileManager:
    """Gestionnaire de profils de configuration par dossier"""
    
    def __init__(self):
        self.logger = Logger()
        self.profiles_dir = 'src/config/profiles'
        self.profiles_cache = {}
        self.load_all_profiles()
    
    def load_all_profiles(self):
        """Charge tous les profils disponibles"""
        if not os.path.exists(self.profiles_dir):
            os.makedirs(self.profiles_dir, exist_ok=True)
            self.logger.warning(f"Dossier profiles créé: {self.profiles_dir}")
            return
        
        for file in os.listdir(self.profiles_dir):
            if file.endswith('.json'):
                profile_name = file[:-5]  # Enlever .json
                try:
                    with open(os.path.join(self.profiles_dir, file), 'r', encoding='utf-8') as f:
                        self.profiles_cache[profile_name] = json.load(f)
                        self.logger.debug(f"Profil chargé: {profile_name}")
                except Exception as e:
                    self.logger.error(f"Erreur chargement profil {profile_name}: {e}")
    
    def get_profile_for_folder(self, folder_name):
        """
        Retourne le profil pour un dossier spécifique
        Cherche d'abord un profil spécifique, sinon utilise global
        """
        # Extraire le nom du sous-dossier
        folder_parts = os.path.normpath(folder_name).split(os.sep)
        
        # Chercher le sous-dossier après 'scan'
        if 'scan' in folder_parts:
            scan_index = folder_parts.index('scan')
            if scan_index + 1 < len(folder_parts):
                subfolder = folder_parts[scan_index + 1]
                
                # Chercher un profil spécifique
                if subfolder in self.profiles_cache:
                    profile = self.profiles_cache[subfolder]
                    self.logger.info(f"Profil '{subfolder}' utilisé pour {folder_name}")
                    
                    # Gérer l'héritage
                    if 'inherits_from' in profile:
                        profile = self.merge_profiles(profile, profile['inherits_from'])
                    
                    return profile
        
        # Utiliser le profil global par défaut
        if 'global' in self.profiles_cache:
            self.logger.info(f"Profil global utilisé pour {folder_name}")
            return self.profiles_cache['global']
        
        # Profil minimal par défaut
        self.logger.warning(f"Aucun profil trouvé pour {folder_name}, utilisation config minimale")
        return self.get_default_profile()
    
    def merge_profiles(self, child_profile, parent_name):
        """Fusionne un profil enfant avec son parent (héritage)"""
        if parent_name not in self.profiles_cache:
            self.logger.warning(f"Profil parent '{parent_name}' non trouvé")
            return child_profile
        
        parent_profile = self.profiles_cache[parent_name].copy()
        
        # Fusion récursive des dictionnaires
        def deep_merge(parent, child):
            result = parent.copy()
            for key, value in child.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = deep_merge(result[key], value)
                elif key in result and isinstance(result[key], list) and isinstance(value, list):
                    # Pour les listes, on combine sans doublons
                    result[key] = list(set(result[key] + value))
                else:
                    result[key] = value
            return result
        
        merged = deep_merge(parent_profile, child_profile)
        return merged
    
    def get_default_profile(self):
        """Retourne un profil minimal par défaut"""
        return {
            'profile_name': 'Default',
            'user_info': {},
            'extraction_settings': {
                'language': 'fra+eng'
            },
            'naming_rules': {
                'format': '{date}_{supplier}_{invoice}',
                'date_format': 'YYYYMMDD',
                'separator': '_'
            }
        }
    
    def save_profile(self, name, profile_data):
        """Sauvegarde ou met à jour un profil"""
        file_path = os.path.join(self.profiles_dir, f"{name}.json")
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(profile_data, f, indent=2, ensure_ascii=False)
            
            # Mettre à jour le cache
            self.profiles_cache[name] = profile_data
            self.logger.info(f"Profil '{name}' sauvegardé")
            return True
        except Exception as e:
            self.logger.error(f"Erreur sauvegarde profil {name}: {e}")
            return False
    
    def get_user_info(self, profile):
        """Extrait les informations utilisateur d'un profil"""
        return profile.get('user_info', {})
    
    def get_extraction_settings(self, profile):
        """Extrait les paramètres d'extraction d'un profil"""
        return profile.get('extraction_settings', {})
    
    def get_supplier_mapping(self, profile, supplier_name):
        """Retourne le nom mappé d'un fournisseur si configuré"""
        mappings = profile.get('supplier_mappings', {})
        
        # Chercher une correspondance exacte ou partielle
        for full_name, short_name in mappings.items():
            if full_name.lower() in supplier_name.lower():
                return short_name
        
        return supplier_name  # Retourner le nom original si pas de mapping
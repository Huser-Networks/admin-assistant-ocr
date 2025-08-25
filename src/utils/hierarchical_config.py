import json
import os
from copy import deepcopy
from src.utils.logger import Logger


class HierarchicalConfig:
    """Gestionnaire de configuration hiérarchique avec héritage et surcharges"""
    
    def __init__(self):
        self.logger = Logger()
        self.config_file = 'src/config/hierarchical_config.json'
        self.config = self.load_config()
    
    def load_config(self):
        """Charge la configuration hiérarchique"""
        if not os.path.exists(self.config_file):
            # Créer une config par défaut
            default = self.create_default_config()
            self.save_config(default)
            return default
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Erreur chargement config hiérarchique: {e}")
            return self.create_default_config()
    
    def create_default_config(self):
        """Crée une configuration par défaut"""
        return {
            "global": {
                "user_info": {
                    "names": [],
                    "addresses": [],
                    "companies": [],
                    "emails": [],
                    "phones": []
                },
                "supplier_mappings": {},
                "keywords_to_ignore": ["destinataire", "client", "livré à"]
            },
            "folders": {}
        }
    
    def save_config(self, config=None):
        """Sauvegarde la configuration"""
        if config is None:
            config = self.config
        
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        self.logger.info("Configuration hiérarchique sauvegardée")
    
    def get_folder_config(self, folder_name):
        """
        Retourne la configuration effective pour un dossier
        en appliquant l'héritage et les surcharges
        """
        
        # Commencer avec la config globale
        effective_config = deepcopy(self.config.get('global', {}))
        
        # Si le dossier a une config spécifique
        if folder_name in self.config.get('folders', {}):
            folder_config = self.config['folders'][folder_name]
            
            # Appliquer les ajouts
            if 'add' in folder_config:
                effective_config = self._merge_add(effective_config, folder_config['add'])
            
            # Appliquer les suppressions
            if 'remove' in folder_config:
                effective_config = self._apply_remove(effective_config, folder_config['remove'])
            
            # Ajouter les métadonnées du dossier
            effective_config['folder_name'] = folder_name
            effective_config['folder_description'] = folder_config.get('description', '')
        
        self.logger.debug(f"Config effective pour {folder_name}: {len(effective_config.get('user_info', {}).get('names', []))} noms")
        
        return effective_config
    
    def _merge_add(self, base_config, additions):
        """Fusionne les ajouts dans la config de base"""
        result = deepcopy(base_config)
        
        for key, value in additions.items():
            if key not in result:
                result[key] = value
            elif isinstance(value, dict) and isinstance(result[key], dict):
                # Fusion récursive pour les dictionnaires
                result[key] = self._merge_add(result[key], value)
            elif isinstance(value, list) and isinstance(result[key], list):
                # Pour les listes, ajouter les éléments uniques
                for item in value:
                    if item not in result[key]:
                        result[key].append(item)
            else:
                # Remplacer la valeur
                result[key] = value
        
        return result
    
    def _apply_remove(self, base_config, removals):
        """Supprime les éléments spécifiés de la config"""
        result = deepcopy(base_config)
        
        for key, value in removals.items():
            if key in result:
                if isinstance(value, dict) and isinstance(result[key], dict):
                    # Suppression récursive dans les dictionnaires
                    for sub_key, sub_value in value.items():
                        if sub_key in result[key]:
                            if isinstance(sub_value, list) and isinstance(result[key][sub_key], list):
                                # Supprimer des éléments spécifiques de la liste
                                for item in sub_value:
                                    if item in result[key][sub_key]:
                                        result[key][sub_key].remove(item)
                            else:
                                # Supprimer la clé entière
                                del result[key][sub_key]
                elif isinstance(value, list) and isinstance(result[key], list):
                    # Supprimer des éléments de la liste
                    for item in value:
                        if item in result[key]:
                            result[key].remove(item)
        
        return result
    
    def is_user_info(self, text, folder_name):
        """
        Vérifie si le texte contient des infos utilisateur
        pour le dossier spécifié
        """
        config = self.get_folder_config(folder_name)
        user_info = config.get('user_info', {})
        
        text_lower = text.lower()
        
        # Vérifier les noms
        for name in user_info.get('names', []):
            if name.lower() in text_lower:
                self.logger.debug(f"Info utilisateur trouvée dans {folder_name}: {name}")
                return True
        
        # Vérifier les adresses
        for address in user_info.get('addresses', []):
            if address.lower() in text_lower:
                self.logger.debug(f"Adresse utilisateur trouvée dans {folder_name}: {address}")
                return True
        
        # Vérifier les entreprises
        for company in user_info.get('companies', []):
            if company.lower() in text_lower:
                self.logger.debug(f"Entreprise utilisateur trouvée dans {folder_name}: {company}")
                return True
        
        return False
    
    def add_folder_config(self, folder_name, description="", add_config=None, remove_config=None):
        """Ajoute ou met à jour la configuration d'un dossier"""
        
        if 'folders' not in self.config:
            self.config['folders'] = {}
        
        folder_config = {
            "description": description,
            "add": add_config or {},
            "remove": remove_config or {}
        }
        
        self.config['folders'][folder_name] = folder_config
        self.save_config()
        
        self.logger.info(f"Configuration ajoutée pour le dossier: {folder_name}")
    
    def update_global_config(self, user_info=None, supplier_mappings=None):
        """Met à jour la configuration globale"""
        
        if 'global' not in self.config:
            self.config['global'] = self.create_default_config()['global']
        
        if user_info:
            self.config['global']['user_info'].update(user_info)
        
        if supplier_mappings:
            self.config['global']['supplier_mappings'].update(supplier_mappings)
        
        self.save_config()
        self.logger.info("Configuration globale mise à jour")
import re
import unicodedata
from datetime import datetime
from src.utils.logger import Logger


class DocumentAnalyzer:
    """Analyse le texte OCR pour extraire les métadonnées du document"""
    
    logger = Logger()
    
    # Patterns pour détecter les dates
    DATE_PATTERNS = [
        # Format français DD/MM/YYYY ou DD-MM-YYYY
        r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b',
        # Format français DD.MM.YYYY
        r'\b(\d{1,2})\.(\d{1,2})\.(\d{4})\b',
        # Format avec mois en texte (ex: 15 janvier 2024)
        r'\b(\d{1,2})\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+(\d{4})\b',
        # Format ISO YYYY-MM-DD
        r'\b(\d{4})[/-](\d{1,2})[/-](\d{1,2})\b',
    ]
    
    # Mots-clés pour identifier les dates importantes
    DATE_KEYWORDS = ['date', 'le', 'émise', 'facture du', 'document du', 'établi', 'échéance']
    
    # Mots-clés pour identifier les numéros de facture
    INVOICE_KEYWORDS = [
        'facture n°', 'facture no', 'facture num', 'invoice',
        'n° facture', 'numéro de facture', 'référence', 'ref.',
        'n°', 'numero', 'num.', 'devis n°', 'commande n°'
    ]
    
    # Mots-clés pour identifier le fournisseur
    SUPPLIER_KEYWORDS = ['sarl', 'sas', 'sa', 'eurl', 'siren', 'siret', 'tva', 'ste', 'société']
    
    MONTHS = {
        'janvier': '01', 'février': '02', 'mars': '03', 'avril': '04',
        'mai': '05', 'juin': '06', 'juillet': '07', 'août': '08',
        'septembre': '09', 'octobre': '10', 'novembre': '11', 'décembre': '12'
    }
    
    @staticmethod
    def extract_date(text):
        """Extrait la date la plus probable du document"""
        text_lower = text.lower()
        found_dates = []
        
        # Chercher toutes les dates dans le texte
        for pattern in DocumentAnalyzer.DATE_PATTERNS:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                # Calculer un score basé sur la proximité avec des mots-clés
                position = match.start()
                score = 0
                
                # Vérifier la proximité avec les mots-clés
                for keyword in DocumentAnalyzer.DATE_KEYWORDS:
                    keyword_pos = text_lower.rfind(keyword, max(0, position - 50), position)
                    if keyword_pos != -1:
                        score += 50 - (position - keyword_pos)
                
                found_dates.append((match, score))
        
        if not found_dates:
            DocumentAnalyzer.logger.debug("Aucune date trouvée dans le document")
            return None
        
        # Trier par score et prendre la meilleure
        found_dates.sort(key=lambda x: x[1], reverse=True)
        best_match = found_dates[0][0]
        
        # Parser la date selon le format
        try:
            groups = best_match.groups()
            
            # Format avec mois en texte
            if len(groups) == 3 and groups[1] in DocumentAnalyzer.MONTHS:
                day = groups[0].zfill(2)
                month = DocumentAnalyzer.MONTHS[groups[1]]
                year = groups[2]
            # Format ISO YYYY-MM-DD
            elif len(groups) == 3 and len(groups[0]) == 4:
                year = groups[0]
                month = groups[1].zfill(2)
                day = groups[2].zfill(2)
            # Format DD/MM/YYYY ou DD-MM-YYYY
            else:
                day = groups[0].zfill(2)
                month = groups[1].zfill(2)
                year = groups[2]
            
            date_str = f"{year}{month}{day}"
            DocumentAnalyzer.logger.debug(f"Date extraite: {date_str}")
            return date_str
            
        except Exception as e:
            DocumentAnalyzer.logger.error(f"Erreur lors du parsing de la date: {e}")
            return None
    
    @staticmethod
    def extract_invoice_number(text):
        """Extrait le numéro de facture ou de référence"""
        text_lower = text.lower()
        
        for keyword in DocumentAnalyzer.INVOICE_KEYWORDS:
            # Chercher le mot-clé
            pos = text_lower.find(keyword)
            if pos != -1:
                # Extraire le texte après le mot-clé
                after_keyword = text[pos + len(keyword):pos + len(keyword) + 50]
                
                # Chercher un numéro (lettres et chiffres)
                match = re.search(r'[\s:]*([A-Z0-9\-/]+)', after_keyword, re.IGNORECASE)
                if match:
                    invoice_num = match.group(1).strip()
                    # Nettoyer le numéro
                    invoice_num = re.sub(r'[^\w\-]', '', invoice_num)
                    if invoice_num:
                        DocumentAnalyzer.logger.debug(f"Numéro de facture extrait: {invoice_num}")
                        return invoice_num
        
        DocumentAnalyzer.logger.debug("Aucun numéro de facture trouvé")
        return None
    
    @staticmethod
    def extract_supplier(text, folder_name=None):
        """Extrait le nom du fournisseur selon le dossier"""
        # Utiliser l'extracteur intelligent avec le nom du dossier
        from src.extractors.supplier_extractor import SupplierExtractor
        extractor = SupplierExtractor(folder_name=folder_name)
        return extractor.extract(text)
    
    @staticmethod  
    def extract_supplier_legacy(text):
        """Ancienne méthode d'extraction (fallback)"""
        lines = text.split('\n')
        
        # Stratégie 1: Chercher dans les premières lignes (souvent l'en-tête)
        for i, line in enumerate(lines[:10]):  # Les 10 premières lignes
            line_lower = line.lower()
            
            # Si la ligne contient un mot-clé d'entreprise
            for keyword in DocumentAnalyzer.SUPPLIER_KEYWORDS:
                if keyword in line_lower:
                    # Nettoyer et prendre le nom
                    supplier = line.strip()
                    # Enlever les infos légales mais garder le nom
                    supplier = re.sub(r'\b(siren|siret|tva|n°tva|rcs).*', '', supplier, flags=re.IGNORECASE)
                    # Garder le nom mais peut-être enlever le type de société à la fin
                    supplier = re.sub(r'\s+(sarl|sas|sa|eurl|sasu|eirl)\s*$', '', supplier, flags=re.IGNORECASE)
                    supplier = supplier.strip()
                    
                    if supplier and len(supplier) > 2:
                        # Limiter la longueur
                        supplier = supplier[:40]
                        DocumentAnalyzer.logger.debug(f"Fournisseur extrait: {supplier}")
                        return supplier
        
        # Stratégie 2: Prendre la première ligne non vide qui semble être un nom
        for line in lines[:5]:
            line = line.strip()
            if len(line) > 3 and len(line) < 50:
                # Vérifier que ce n'est pas une date ou un numéro
                if not re.match(r'^[\d\s/\-\.]+$', line):
                    supplier = line.strip()[:40]
                    if supplier:
                        DocumentAnalyzer.logger.debug(f"Fournisseur supposé: {supplier}")
                        return supplier
        
        DocumentAnalyzer.logger.debug("Aucun fournisseur trouvé")
        return "Document"
    
    @staticmethod
    def remove_accents(text):
        """Remplace les caractères accentués par leur équivalent sans accent"""
        # Normaliser en NFD (décomposition) puis filtrer les accents
        nfd = unicodedata.normalize('NFD', text)
        without_accents = ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')
        return without_accents
    
    @staticmethod
    def to_camel_case(text):
        """Convertit un texte en CamelCase"""
        # Enlever les accents d'abord
        text = DocumentAnalyzer.remove_accents(text)
        # Diviser par espaces, underscores, tirets
        words = re.split(r'[\s_\-]+', text)
        # Capitaliser chaque mot et joindre
        camel = ''.join(word.capitalize() for word in words if word)
        return camel
    
    @staticmethod
    def clean_filename_part(text, use_camel_case=True):
        """Nettoie une partie du nom de fichier"""
        # Enlever les accents
        text = DocumentAnalyzer.remove_accents(text)
        
        if use_camel_case:
            # Convertir en CamelCase
            return DocumentAnalyzer.to_camel_case(text)
        else:
            # Ancien comportement avec underscores
            text = re.sub(r'[^\w\-]', '_', text)
            text = re.sub(r'_{2,}', '_', text)
            text = text.strip('_')
            return text
    
    @staticmethod
    def generate_filename(text, original_filename=None, folder_name=None):
        """
        Génère un nom de fichier intelligent basé sur le contenu OCR
        Format: YYYYMMDD_Fournisseur_NumeroFacture.pdf
        """
        # Extraire les métadonnées avec contexte de dossier
        date = DocumentAnalyzer.extract_date(text)
        supplier = DocumentAnalyzer.extract_supplier(text, folder_name=folder_name)
        invoice_num = DocumentAnalyzer.extract_invoice_number(text)
        
        # Si pas de date, utiliser la date du jour
        if not date:
            date = datetime.now().strftime('%Y%m%d')
            DocumentAnalyzer.logger.info("Pas de date trouvée, utilisation de la date du jour")
        
        # Construire le nom de fichier en CamelCase
        parts = [date]  # La date reste en format YYYYMMDD
        
        if supplier:
            # Nettoyer le nom du fournisseur en CamelCase
            supplier_clean = DocumentAnalyzer.clean_filename_part(supplier, use_camel_case=True)
            if supplier_clean:
                parts.append(supplier_clean)
        
        if invoice_num:
            # Pour les numéros, garder le format original mais nettoyer
            invoice_clean = DocumentAnalyzer.remove_accents(invoice_num)
            invoice_clean = re.sub(r'[^\w\-]', '', invoice_clean)
            if invoice_clean:
                parts.append(invoice_clean)
        
        # Si on n'a que la date, ajouter un identifiant générique
        if len(parts) == 1:
            parts.append('Document')
        
        # Joindre toutes les parties avec des underscores
        filename = '_'.join(parts) + '.pdf'
        
        DocumentAnalyzer.logger.info(f"Nom de fichier généré: {filename}")
        return filename
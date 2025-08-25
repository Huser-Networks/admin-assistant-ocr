# src/controllers/ocr_controller.py
import os
import json
import platform
import shutil
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
from src.utils.logger import Logger
from src.utils.document_analyzer import DocumentAnalyzer
from src.utils.learning_system import LearningSystem

# Configuration pour Windows
if platform.system() == 'Windows':
    # Chemins typiques de Tesseract sur Windows
    tesseract_paths = [
        r'C:\Tools\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        r'C:\Tesseract-OCR\tesseract.exe',
    ]
    
    for path in tesseract_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            break


class OCRController:
    logger = Logger()
    learning_system = LearningSystem()
    
    @staticmethod
    def pdf_to_images(pdf_path):
        OCRController.logger.info(f"Converting PDF to images: {pdf_path}")
        try:
            # Sur Windows, spécifier le chemin de poppler si nécessaire
            if platform.system() == 'Windows':
                poppler_paths = [
                    r'C:\Tools\poppler\Library\bin',
                    r'C:\poppler\Library\bin',
                    r'C:\Program Files\poppler\bin',
                ]
                poppler_path = None
                for path in poppler_paths:
                    if os.path.exists(path):
                        poppler_path = path
                        break
                
                if poppler_path:
                    images = convert_from_path(pdf_path, poppler_path=poppler_path)
                else:
                    images = convert_from_path(pdf_path)
            else:
                images = convert_from_path(pdf_path)
            
            OCRController.logger.debug(f"Successfully converted {len(images)} pages")
        except Exception as e:
            OCRController.logger.error(f"Error converting PDF {pdf_path}: {e}")
            images = []
        return images

    @staticmethod
    def ocr_image(image):
        try:
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            OCRController.logger.error(f"Error during OCR: {e}")
            return ""

    @staticmethod
    def process_pdf(pdf_path, output_folder="output"):
        OCRController.logger.info(f"Starting OCR process for: {pdf_path}")
        
        # Extraire le texte via OCR
        images = OCRController.pdf_to_images(pdf_path)
        if not images:
            OCRController.logger.warning(f"No images extracted from {pdf_path}")
            return None
            
        all_text = []
        
        for i, image in enumerate(images):
            OCRController.logger.debug(f"Processing page {i+1}/{len(images)}")
            text = OCRController.ocr_image(image)
            if text:
                all_text.append(text)
        
        if not all_text:
            OCRController.logger.warning(f"No text extracted from {pdf_path}")
            return None
        
        # Analyser le texte pour générer un nom intelligent
        full_text = '\n'.join(all_text)
        original_filename = os.path.basename(pdf_path)
        
        # Extraire le nom du dossier depuis le chemin
        folder_name = None
        path_parts = os.path.normpath(pdf_path).split(os.sep)
        if 'scan' in path_parts:
            scan_index = path_parts.index('scan')
            if scan_index + 1 < len(path_parts):
                folder_name = path_parts[scan_index + 1]
        
        new_filename = DocumentAnalyzer.generate_filename(full_text, original_filename, folder_name)
        
        # Déterminer le sous-dossier de sortie (garder la même structure)
        # Extraire le chemin relatif depuis scan/
        path_parts = os.path.normpath(pdf_path).split(os.sep)
        if 'scan' in path_parts:
            scan_index = path_parts.index('scan')
            # Récupérer les sous-dossiers après 'scan'
            sub_folders = path_parts[scan_index + 1:-1]  # Exclure 'scan' et le nom de fichier
            
            # Créer le chemin de sortie avec la même structure
            output_subfolder = os.path.join(output_folder, *sub_folders) if sub_folders else output_folder
        else:
            output_subfolder = output_folder
        
        # Créer le dossier de sortie si nécessaire
        os.makedirs(output_subfolder, exist_ok=True)
        
        # Copier le PDF avec le nouveau nom
        output_path = os.path.join(output_subfolder, new_filename)
        
        try:
            shutil.copy2(pdf_path, output_path)
            OCRController.logger.info(f"✓ PDF copié et renommé: {output_path}")
            
            # Enregistrer pour apprentissage
            extracted_data = {
                'date': new_filename.split('_')[0],
                'supplier': extracted.get('supplier'),
                'invoice': extracted.get('invoice'),
                'original_text': full_text[:1000]  # Premiers 1000 caractères
            }
            
            OCRController.learning_system.record_extraction(
                pdf_path, full_text, extracted_data, new_filename
            )
            
            # Sauvegarder pour révision potentielle  
            try:
                import sys
                sys.path.append('scripts')
                from review_results import ReviewInterface
                review = ReviewInterface()
                review.save_extraction_for_review(pdf_path, full_text, extracted_data, new_filename)
            except ImportError:
                # Si l'import échoue, continuer sans sauvegarder pour révision
                pass
            
            return output_path
        except Exception as e:
            OCRController.logger.error(f"Erreur lors de la copie du PDF: {e}")
            return None


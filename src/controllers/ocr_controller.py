# src/controllers/ocr_controller.py
import os
import json
import platform
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
from src.utils.logger import Logger

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
        
        # Save results
        if all_text:
            os.makedirs(output_folder, exist_ok=True)
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            output_path = os.path.join(output_folder, f"{base_name}.txt")
            
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(all_text))
                OCRController.logger.info(f"✓ OCR results saved to: {output_path}")
                return output_path
            except Exception as e:
                OCRController.logger.error(f"Failed to save results: {e}")
                return None
        else:
            OCRController.logger.warning(f"No text extracted from {pdf_path}")
            return None


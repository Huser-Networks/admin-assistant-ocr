# src/controllers/ocr_controller.py
from PIL import Image
from pdf2image import convert_from_path
import pytesseract


class OCRController:
    @staticmethod
    def pdf_to_images(pdf_path):
        print(f"Converting PDF to images: {pdf_path}")
        try:
            images = convert_from_path(pdf_path)
        except Exception as e:
            print(f"Error converting PDF: {e}")
            images = []
        print(f"Number of images: {len(images)}")
        return images

    @staticmethod
    def ocr_image(image):
        return pytesseract.image_to_string(image)

    @staticmethod
    def process_pdf(pdf_path):
        images = OCRController.pdf_to_images(pdf_path)
        for image in images:
            print(f"Processing image: {image}")
            text = OCRController.ocr_image(image)


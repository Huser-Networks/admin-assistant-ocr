import os
import sys
from functools import partial

from src.controllers.config_controller import ConfigController
from src.controllers.file_controller import FileController
from src.controllers.ocr_controller import OCRController
from src.utils.concurrent_manager import ConcurrentManager
from src.utils.logger import Logger


def main():
    logger = Logger()
    logger.info("Starting OCR Assistant...")
    
    try:
        # Load configuration
        config = ConfigController.load_config()
        scan_folder = config.get('scan_folder', 'scan')
        sub_folders = config.get('sub_folders', [])
        output_folder = config.get('output_folder', 'output')
        
        if not sub_folders:
            logger.error("No sub_folders configured in config.json")
            return
        
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        
        # Create a partial function with the output folder
        process_pdf_with_output = partial(OCRController.process_pdf, output_folder=output_folder)
        
        total_files_processed = 0
        
        # Explore each sub-folder
        for sub_folder in sub_folders:
            folder_path = os.path.join(scan_folder, sub_folder)
            logger.info(f"Processing folder: {folder_path}")
            
            files = FileController.explore_folder(folder_path)
            
            if files:
                ConcurrentManager.process_files(files, process_pdf_with_output)
                total_files_processed += len(files)
            else:
                logger.warning(f"No PDF files found in {folder_path}")
        
        logger.info(f"✓ Total files processed: {total_files_processed}")
        logger.info("OCR processing completed successfully")
        
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found - {e}")
        sys.exit(1)
    except KeyError as e:
        logger.error(f"Missing configuration key - {e}")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

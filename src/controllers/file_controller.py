import os
from src.utils.logger import Logger


class FileController:
    logger = Logger()
    
    @staticmethod
    def explore_folder(folder_path, file_extensions=['.pdf']):
        files_found = []
        
        if not os.path.exists(folder_path):
            FileController.logger.warning(f"Folder does not exist: {folder_path}")
            return files_found
            
        for subdir, _, files in os.walk(folder_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in file_extensions):
                    file_path = os.path.join(subdir, file)
                    files_found.append(file_path)
                    FileController.logger.debug(f"Found: {file_path}")
        
        FileController.logger.info(f"Found {len(files_found)} PDF file(s) in {folder_path}")
        return files_found

import os

from src.controllers.config_controller import ConfigController
from src.controllers.file_controller import FileController
from src.controllers.ocr_controller import OCRController
from src.utils.concurrent_manager import ConcurrentManager


def main():
    config = ConfigController.load_config()
    scan_folder = config['scan_folder']
    sub_folders = config['sub_folders']

    # Explore each sub-folder
    for sub_folder in sub_folders:
        folder_path = os.path.join(scan_folder, sub_folder)
        files = FileController.explore_folder(folder_path)
        ConcurrentManager.process_files(files, OCRController.process_pdf)


if __name__ == '__main__':
    main()

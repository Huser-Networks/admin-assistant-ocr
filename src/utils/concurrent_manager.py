# src/utils/concurrent_manager.py
from concurrent.futures import ThreadPoolExecutor


class ConcurrentManager:
    @staticmethod
    def process_files(files, processing_function):
        with ThreadPoolExecutor() as executor:
            executor.map(processing_function, files)

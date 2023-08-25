import os


class FileController:
    @staticmethod
    def explore_folder(folder_path):
        files_found = []
        for subdir, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(subdir, file)
                files_found.append(file_path)
        print(f"Found file: {files_found.__len__()}")
        return files_found

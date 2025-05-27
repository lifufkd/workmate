import os


class JsonManager:
    def __init__(self):
        pass

    @staticmethod
    def write_file(file_path: str, file_data: bytes) -> None:
        with open(file_path, "wb") as f:
            f.write(file_data)

    @staticmethod
    def read_file(file_path: str) -> bytes:
        with open(file_path, "rb") as f:
            return f.read()

    @staticmethod
    def delete_file(file_path: str) -> None:
        if JsonManager.file_exists(file_path):
            os.remove(file_path)

    @staticmethod
    def file_exists(file_path: str) -> bool:
        return os.path.isfile(file_path)

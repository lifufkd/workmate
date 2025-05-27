import os


class CsvManager:
    def __init__(self):
        pass

    @staticmethod
    def read_file(file_path: str) -> str:
        with open(file_path, "r") as f:
            return f.read()

    @staticmethod
    def process_file(file_path: str) -> list[dict]:
        result = list()
        csv_data = CsvManager.read_file(file_path)

        rows = csv_data.split("\n")
        rows = [i.split(",") for i in rows]

        for row in rows[1:]:
            result.append(dict(zip(rows[0], row)))

        return result

    @staticmethod
    def file_exists(file_path: str) -> bool:
        return os.path.isfile(file_path)

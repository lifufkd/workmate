import json


class JsonManager:
    def __init__(self):
        pass

    @staticmethod
    def write_file(file_path: str, file_data: dict) -> None:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(file_data, indent=4, sort_keys=True))

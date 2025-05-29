import json


class JsonManager:
    def __init__(self):
        pass

    def write_file(self, file_path: str, file_data: dict) -> None:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json.dumps(file_data, indent=4, sort_keys=True))

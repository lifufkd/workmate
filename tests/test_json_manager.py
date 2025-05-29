import json
from src.file_managers.json_manager import JsonManager
from unittest.mock import patch


class TestJsonManager:

    def test_write_file(self, tmp_path):
        json_manager = JsonManager()
        file_path = tmp_path / "test.json"
        test_data = {"a": 1, "b": 2}
        expected_content = json.dumps(test_data, indent=4, sort_keys=True)

        json_manager.write_file(str(file_path), test_data)

        assert file_path.exists()
        assert file_path.is_file()
        assert file_path.read_text(encoding="utf-8") == expected_content



from src.file_managers.csv_manager import CsvManager
from unittest.mock import patch


class TestCsvManager:

    def test_read_file(self, tmp_path):
        file_path = tmp_path / "sample.csv"
        content = "name,age\nAlice,30\nBob,25"
        file_path.write_text(content)

        result = CsvManager().read_file(str(file_path))
        assert result == content

    @patch("src.file_managers.csv_manager.CsvManager.read_file", return_value="name,age\nAlice,30\nBob,25")
    def test_process_file(self, monkeypatch):
        result = CsvManager().process_file("dummy.csv")
        assert result == [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]

    @patch("src.file_managers.csv_manager.CsvManager.read_file", return_value="")
    def test_process_file_empty(self, monkeypatch):
        result = CsvManager().process_file("empty.csv")
        assert result == []  # потому что rows[1:] будет пустой

    def test_file_exists(self, tmp_path):
        csv_manager = CsvManager()
        file_path = tmp_path / "exists.csv"
        file_path.write_text("name,age\n")

        assert csv_manager.file_exists(str(file_path)) is True
        assert csv_manager.file_exists("non_existent.csv") is False

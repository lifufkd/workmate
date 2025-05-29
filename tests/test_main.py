import pytest
import json

from src.main import (
    check_files_is_existed,
    process_data,
    export_data,
    pretty_print_data
)


@pytest.fixture
def sample_employees_data():
    return [
        {
             "id": 1,
             "email": "alice@example.com",
             "name": "Alice",
             "department": "Marketing",
             "hours_worked": "160",
             "hourly_rate": "50"
        },
        {
             "id": 2,
             "email": "bob@example.com",
             "name": "Bob",
             "department": "Design",
             "hours_worked": "150",
             "hourly_rate": "40"
        },
        {
             "id": 3,
             "email": "carol@example.com",
             "name": "Carol",
             "department": "Design",
             "hours_worked": "170",
             "hourly_rate": "60"
         }
    ]


def test_check_files_is_existed_all_valid(tmp_path):
    file1 = tmp_path / "file1.csv"
    file2 = tmp_path / "file2.csv"
    file1.write_text("")
    file2.write_text("")
    check_files_is_existed([str(file1), str(file2)])


def test_process_data_valid(sample_employees_data):
    result = process_data("payout", sample_employees_data)
    assert isinstance(result, dict)

    # Check valid of summary data
    assert result["Marketing"]["summary"] == {"worked_hours": 160, "payout": 8000}
    assert result["Design"]["summary"] == {"worked_hours": 320, "payout": 16200}

    # Employees sorted by payout
    assert result["Design"]["employees"][0]["name"] == "Bob"
    assert result["Design"]["employees"][1]["name"] == "Carol"
    # Departments sorted by alphabet
    assert list(result.keys())[0] == "Design"


def test_process_data_invalid_mode(sample_employees_data):
    with pytest.raises(NotImplementedError):
        process_data("unknown_mode", sample_employees_data)


def test_export_data_json(tmp_path):
    export_path = tmp_path / "report.json"
    data = {"some": "data"}
    export_data("JSON", str(export_path), data)

    assert export_path.exists()
    content = json.loads(export_path.read_text())
    assert content == data


def test_export_data_invalid_format():
    with pytest.raises(NotImplementedError) as e:
        export_data("XML", "", {"a": 1})
        assert f"Export method 'XML' is not implemented! Error in saving report" in e


def test_pretty_print_data_prints():
    input_data = {
        "Design": {
            "employees": [
                {
                    "name": "Bob Smith",
                    "hours_worked": "150",
                    "hourly_rate": "40",
                    "payout": 6000
                }
            ],
            "summary": {
                "worked_hours": 150,
                "payout": 6000
            }
        }
    }
    processed_data = pretty_print_data(input_data)
    assert "Design" in processed_data
    assert "Bob Smith" in processed_data
    assert "$" in processed_data
    assert "6,000" in processed_data

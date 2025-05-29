import pytest
from src.report_handlers.payout import PayoutHandler


@pytest.fixture
def handler():
    return PayoutHandler()


@pytest.mark.parametrize(
    "field",
    [
        "hourly_rate",
        "rate",
        "salary"
    ]
                         )
def test_calculate_payout_with_alternative_fields(handler, field):
    employee = {field: "60", "hours_worked": "100"}
    assert handler._calculate_payout(employee) == 6000


def test_calculate_payout_missing_rate(handler):
    employee = {"hours_worked": "100"}
    assert handler._calculate_payout(employee) is None


def test_calculate_payout_invalid_format(handler):
    employee = {"hourly_rate": "fifty", "hours_worked": "one hundred"}
    assert handler._calculate_payout(employee) is None


def test_sort_and_aggregate_by_payout(handler):
    data = {
        "Marketing": {
            "employees": [
                {"name": "Alice", "hours_worked": "160", "payout": 8000}
            ]
        },
        "Design": {
            "employees": [
                {"name": "Carol", "hours_worked": "170", "payout": 10200},
                {"name": "Bob", "hours_worked": "150", "payout": 6000},
            ]
        }
    }

    result = handler._sort_and_aggregate_by_payout(data)
    assert list(result.keys()) == ["Design", "Marketing"]
    # Check valid of summary data by department
    assert result["Design"]["summary"] == {"worked_hours": 320, "payout": 16200}
    assert result["Marketing"]["summary"] == {"worked_hours": 160, "payout": 8000}
    # Employees sorted by payout
    assert result["Design"]["employees"][0]["name"] == "Bob"
    # Departments sorted by alphabet
    assert list(result.keys())[0] == "Design"


def test_process_data_full(handler):
    employees = [
        {"id": 1, "email": "alice@example.com", "name": "Alice", "department": "Marketing", "hours_worked": "160", "hourly_rate": "50"},
        {"id": 2, "email": "bob@example.com", "name": "Bob", "department": "Design", "hours_worked": "150", "hourly_rate": "40"},
        {"id": 3, "email": "carol@example.com", "name": "Carol", "department": "Design", "hours_worked": "170", "hourly_rate": "60"},
    ]

    result = handler.process_data(employees)

    assert list(result.keys()) == ["Design", "Marketing"]

    # Check valid of summary data
    assert result["Marketing"]["summary"] == {"worked_hours": 160, "payout": 8000}
    assert result["Design"]["summary"] == {"worked_hours": 320, "payout": 16200}

    # Employees sorted by payout
    assert result["Design"]["employees"][0]["name"] == "Bob"
    assert result["Design"]["employees"][1]["name"] == "Carol"
    # Departments sorted by alphabet
    assert list(result.keys())[0] == "Design"


def test_process_data_with_invalid_and_missing(handler):
    employees = [
        {"id": 1, "email": "bad@example.com", "name": "Bad", "department": "Marketing", "hours_worked": "160", "hourly_rate": "invalid"},
        {"id": 2, "email": "no_rate@example.com", "name": "Missing", "department": "Design", "hours_worked": "150"},
        {"id": 3, "email": "valid@example.com", "name": "Good", "department": "HR", "hours_worked": "100", "salary": "70"},
    ]

    result = handler.process_data(employees)

    # Check for only 'HR' department in result
    assert list(result.keys()) == ["HR"]

    assert result["HR"]["summary"] == {"worked_hours": 100, "payout": 7000}

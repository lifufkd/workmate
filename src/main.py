import argparse
import sys

from file_manager.csv import CsvManager
from reports_handlers.payout import PayoutHandler


def check_files_is_existed(files_paths: list[str]) -> None:
    invalid_paths = list()

    for path in files_paths:
        if not CsvManager.file_exists(path):
            invalid_paths.append(path)

    if invalid_paths:
        sys.exit(
            "Error read files: " + ", ".join(invalid_paths)
        )


def process_data(report_mode: str, raw_empoyees_data: list[dict]) -> dict:
    match report_mode:
        case "payout":
            processed_data = PayoutHandler.process_employees_data(raw_empoyees_data)
        case _:
            processed_data = []

    return processed_data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Workers stats calculator")

    parser.add_argument(
        "employees_files",
        nargs="+",
        help="Workers data in CSV format",
    )
    parser.add_argument(
        "--report",
        choices=["payout"],  # Can be extended in future
        required=True,
        help="Generated report type"
    )

    return parser.parse_args()


def main():
    employees_data = list()
    args = parse_args()

    # Validate is files existed (easily can be extended to check validity of file structure)
    check_files_is_existed(files_paths=args.employees_files)

    # Loading all raw employees data from csv's
    for employees_file in args.employees_files:
        pert_emp_data = CsvManager.process_file(employees_file)
        employees_data.extend(pert_emp_data)

    # Process raw data
    processed_employees_data = process_data(args.report, employees_data)
    # print(processed_employees_data)


if __name__ == '__main__':
    main()

import argparse
import sys

from file_managers.csv_manager import CsvManager
from file_managers.json_manager import JsonManager
from report_handlers.payout import PayoutHandler


def check_files_is_existed(files_paths: list[str]) -> None:
    invalid_paths = list()

    for path in files_paths:
        if not CsvManager.file_exists(path):
            invalid_paths.append(path)

    if invalid_paths:
        sys.exit(
            "Error read files: " + ", ".join(invalid_paths)
        )


def process_data(report_mode: str, raw_employees_data: list[dict]) -> dict:
    match report_mode:
        case "payout":
            processed_data = PayoutHandler().process_data(raw_employees_data)
        case _:
            raise NotImplemented

    return processed_data


def export_data(report_type: str, save_path:str, processed_employees_data: dict) -> None:
    try:
        match report_type:
            case "JSON":
                JsonManager.write_file(file_path=save_path, file_data=processed_employees_data)
            case _:
                raise NotImplemented
    except (OSError, ValueError, TypeError, UnicodeEncodeError) as e:
        print(f"Error in saving report: {e}")


def pretty_print_data(data: dict) -> None:
    lines = []
    header = f"{' ':<20} {'name':<15} {'hours':>5} {'rate':>5} {'payout':>8}"

    for department_name, department_data in data.items():
        lines.append(department_name)
        # Add header with fields names in each department
        lines.append(header)

        employees = department_data.get("employees", [])
        # Add all employee of current department
        for employee in employees:
            name = employee.get("name", "")
            hours = employee.get("hours_worked", "")
            rate = employee.get("hourly_rate") or employee.get("rate") or employee.get("salary") or ""
            payout = employee.get("payout", 0)
            lines.append(f"{'-' * 20} {name:<15} {hours:>3} {rate:>5} {'$':>3} {payout:>0,}")

        # Add summary data of department
        summary = department_data.get("summary", {})
        total_hours = summary.get("worked_hours", 0)
        total_payout = summary.get("payout", 0)
        lines.append(f"{' ':<20} {total_hours:>19} {'$':>9} {total_payout:>0,}")
        lines.append("")  # Place empty line between departments

    print("\n".join(lines))


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

    parser.add_argument(
        "--export-type",
        choices=["JSON"],
        default="JSON",
        help="Type of report to generate"
    )

    parser.add_argument(
        "--export-file-name",
        required=False,
        default=None,
        help="Can be specified for enabling export generated report"
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

    # Rendering & print report in terminal
    pretty_print_data(processed_employees_data)

    # Optionally exporting report in file
    if args.export_file_name:
        export_data(
            report_type=args.export_type,
            save_path=args.export_file_name,
            processed_employees_data=processed_employees_data
        )


if __name__ == '__main__':
    main()

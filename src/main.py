import argparse
import sys

from file_manager.csv import CsvManager


def check_files_is_existed(files_paths: list[str]) -> None:
    invalid_paths = list()

    for path in files_paths:
        if not CsvManager.file_exists(path):
            invalid_paths.append(path)

    if invalid_paths:
        sys.exit(
            "Error read files: " + ", ".join(invalid_paths)
        )


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
    args = parse_args()

    # Validate is files existed (easily can be extended to check validity of file structure)
    check_files_is_existed(files_paths=args.employees_files)
    CsvManager.process_file(args.employees_files[0])
    print(args)


if __name__ == '__main__':
    main()

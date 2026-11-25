
import csv
from pathlib import Path

CSV_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "facility_service_research.csv"
)

REQUIRED_COLUMNS = [
    "facility_name",
    "city",
    "address",
    "service_name",
    "service_code",
    "source_url",
    "verification_status",
]

ALLOWED_STATUSES = {
    "SOURCE_FOUND_NEEDS_REVIEW",
    "VERIFIED",
    "UNVERIFIED",
}


def validate_csv():
    if not CSV_PATH.exists():
        print("ERROR: CSV file was not found.")
        print("Expected location:", CSV_PATH)
        return False

    errors = []
    seen_records = set()

    # Ignore blank lines before or between CSV records.
    with CSV_PATH.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        non_empty_lines = (line for line in file if line.strip())
        reader = csv.DictReader(non_empty_lines)

        if not reader.fieldnames:
            print("ERROR: CSV file is empty or has no header.")
            return False

        reader.fieldnames = [
            name.strip() for name in reader.fieldnames
        ]

        missing_columns = [
            column for column in REQUIRED_COLUMNS
            if column not in reader.fieldnames
        ]

        if missing_columns:
            print("ERROR: Missing columns:", missing_columns)
            return False

        row_count = 0

        for line_number, row in enumerate(reader, start=2):
            row_count += 1

            row = {
                key.strip(): (value or "").strip()
                for key, value in row.items()
                if key is not None
            }

            missing_values = [
                column for column in REQUIRED_COLUMNS
                if not row.get(column)
            ]

            if missing_values:
                errors.append(
                    f"Line {line_number}: empty fields "
                    f"{missing_values}"
                )
                continue

            if row["verification_status"] not in ALLOWED_STATUSES:
                errors.append(
                    f"Line {line_number}: invalid verification status "
                    f"{row['verification_status']!r}"
                )

            record_key = (
                row["facility_name"].casefold(),
                row["city"].casefold(),
                row["service_code"].upper(),
            )

            if record_key in seen_records:
                errors.append(
                    f"Line {line_number}: duplicate facility-service record"
                )
            else:
                seen_records.add(record_key)

            service_code = row["service_code"]

            if not all(
                char.isalnum() or char == "_"
                for char in service_code
            ):
                errors.append(
                    f"Line {line_number}: invalid service code "
                    f"{service_code!r}"
                )

    print("\nFacility CSV Validation")
    print("========================")
    print("File:", CSV_PATH)
    print("Data rows checked:", row_count)

    if errors:
        print("\nValidation errors:")
        for error in errors:
            print("-", error)

        print("\nPlease correct these issues before importing.")
        return False

    print("No structural or duplicate-record errors found.")
    print(
        "Reminder: passing validation does not verify "
        "the accuracy of the listed hospital services."
    )
    return True


if __name__ == "__main__":
    validate_csv()

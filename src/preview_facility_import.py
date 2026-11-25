
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


def preview_import():
    if not CSV_PATH.exists():
        print("ERROR: CSV file not found:", CSV_PATH)
        return

    with CSV_PATH.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        non_empty_lines = (
            line for line in file if line.strip()
        )
        reader = csv.DictReader(non_empty_lines)

        if not reader.fieldnames:
            print("ERROR: CSV header is missing.")
            return

        reader.fieldnames = [
            name.strip() for name in reader.fieldnames
        ]

        missing_columns = [
            column for column in REQUIRED_COLUMNS
            if column not in reader.fieldnames
        ]

        if missing_columns:
            print("ERROR: Missing columns:", missing_columns)
            return

        rows = list(reader)

    print("\nFACILITY IMPORT PREVIEW")
    print("=======================")
    print("Records found:", len(rows))
    print("Database changes: NONE")
    print()

    for number, row in enumerate(rows, start=1):
        row = {
            key.strip(): (value or "").strip()
            for key, value in row.items()
            if key is not None
        }

        print(f"Record {number}")
        print("Facility:", row["facility_name"])
        print("City:", row["city"])
        print("Service:", row["service_name"])
        print("Service code:", row["service_code"])
        print("Source:", row["source_url"])
        print("Research status:", row["verification_status"])

        if row["verification_status"] == "VERIFIED":
            print(
                "Import decision: REVIEW REQUIRED before approval"
            )
        else:
            print(
                "Import decision: DO NOT mark service as verified"
            )

        print("-" * 45)

    print("\nPreview complete. No database records were changed.")
    print(
        "Note: This script previews data only; it does not "
        "confirm that hospital services are actually available."
    )


if __name__ == "__main__":
    preview_import()

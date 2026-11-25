
import csv
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import engine
from src.research_models import FacilityResearch


CSV_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "raw"
    / "facility_service_research.csv"
)


def make_key(facility_name, city, service_code):
    return (
        facility_name.strip().casefold(),
        city.strip().casefold(),
        service_code.strip().upper(),
    )


def import_research(dry_run=True):
    with CSV_PATH.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        non_empty_lines = (
            line for line in file if line.strip()
        )
        reader = csv.DictReader(non_empty_lines)
        rows = list(reader)

    inserted = 0
    skipped = 0

    with Session(engine) as session:
        existing_records = session.scalars(
            select(FacilityResearch)
        ).all()

        existing_keys = {
            make_key(
                record.facility_name,
                record.city,
                record.service_code,
            )
            for record in existing_records
        }

        for row in rows:
            facility_name = row["facility_name"].strip()
            city = row["city"].strip()
            address = row["address"].strip()
            service_name = row["service_name"].strip()
            service_code = row["service_code"].strip()
            source_url = row["source_url"].strip()

            key = make_key(
                facility_name, city, service_code
            )

            if key in existing_keys:
                skipped += 1
                continue

            print(
                "NEW RECORD:",
                facility_name,
                "|",
                service_name,
                "|",
                service_code,
            )

            if not dry_run:
                record = FacilityResearch(
                    facility_name=facility_name,
                    city=city,
                    address=address,
                    service_name=service_name,
                    service_code=service_code,
                    source_url=source_url,
                    verification_status="SOURCE_FOUND_NEEDS_REVIEW",
                    is_approved=False,
                )

                session.add(record)
                existing_keys.add(key)

            inserted += 1

        if dry_run:
            print("\nDRY RUN: No database changes made.")
            session.rollback()
        else:
            session.commit()
            print("\nImport committed.")

    print("CSV records:", len(rows))
    print("New records:", inserted)
    print("Existing records skipped:", skipped)
    print("Dry run:", dry_run)


if __name__ == "__main__":
    import_research(dry_run=True)

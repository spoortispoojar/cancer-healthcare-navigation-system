
"""
Add missing hospitals from facility_research to facilities.

Default: DRY RUN. No database changes.
Use --apply only after checking the preview.
"""

import argparse

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import engine
from src.models import Facility
from src.research_models import FacilityResearch


EXPECTED_HOSPITALS = {
    "Apollo Cancer Centre",
    "Aster CMI Hospital",
    "HCG Cancer Hospital - Double Road",
    "Kidwai Memorial Institute of Oncology",
    "Manipal Hospital - Old Airport Road",
    "Mazumdar Shaw Medical Centre",
    "Ramaiah Medical College Hospital",
    "Sri Shankara Cancer Hospital & Research Centre",
    "St. John's Medical College Hospital",
    "Vydehi Cancer Centre",
}


def normalize(value):
    return " ".join(value.casefold().split())


def add_researched_facilities(apply=False):
    with Session(engine) as session:
        research_rows = session.execute(
            select(
                FacilityResearch.facility_name,
                FacilityResearch.city,
                FacilityResearch.address,
            ).distinct()
        ).all()

        grouped = {}

        for name, city, address in research_rows:
            key = normalize(name)
            grouped.setdefault(key, set()).add(
                (name, city, address)
            )

        existing = session.scalars(select(Facility)).all()

        existing_by_name = {
            (normalize(f.name), normalize(f.city)): f
            for f in existing
        }

        planned = []

        for expected_name in sorted(EXPECTED_HOSPITALS):
            key = normalize(expected_name)
            records = grouped.get(key, set())

            if not records:
                raise ValueError(
                    f"No research record found for {expected_name}"
                )

            if len(records) != 1:
                raise ValueError(
                    f"Inconsistent research details for {expected_name}: "
                    f"{records}"
                )

            name, city, address = next(iter(records))

            existing_facility = existing_by_name.get(
                (normalize(name), normalize(city))
            )

            if existing_facility:
                if normalize(existing_facility.address or "") != normalize(address):
                    raise ValueError(
                        f"Address mismatch for {name}. "
                        "Manual review required."
                    )

                print(f"ALREADY EXISTS: {name}")
                continue

            planned.append((name, city, address))
            print(f"CREATE: {name} | {city} | {address}")

        print("\nNew facilities planned:", len(planned))

        if not apply:
            print("DRY RUN: No database changes made.")
            return

        for name, city, address in planned:
            session.add(
                Facility(
                    name=name,
                    city=city,
                    address=address,
                    latitude=None,
                    longitude=None,
                )
            )

        session.commit()
        print("Hospital facilities added successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    try:
        add_researched_facilities(apply=args.apply)
    finally:
        engine.dispose()

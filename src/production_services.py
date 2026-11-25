
"""
Production healthcare service categories.

These are real service categories for the hospital recommendation system.
They are separate from the fictional TEST_* service categories.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import engine
from src.models import HealthcareService


PRODUCTION_SERVICES = [
    {
        "service_code": "CHEMOTHERAPY",
        "service_name": "Chemotherapy",
        "description": "Chemotherapy service for cancer treatment.",
    },
    {
        "service_code": "RADIATION",
        "service_name": "Radiation Therapy",
        "description": "Radiation therapy service for cancer treatment.",
    },

    {
        "service_code": "IMMUNOTHERAPY",
        "service_name": "Immunotherapy",
        "description": "Immunotherapy service for cancer treatment.",
    },
    {
        "service_code": "MEDICAL_ONCOLOGY",
        "service_name": "Medical Oncology",
        "description": "Medical oncology services for cancer patients.",
    },
    {
        "service_code": "SURGICAL_ONCOLOGY",
        "service_name": "Surgical Oncology",
        "description": "Surgical oncology services for cancer patients.",
    },
    {
        "service_code": "RADIATION_ONCOLOGY",
        "service_name": "Radiation Oncology",
        "description": "Radiation oncology services for cancer patients.",
    },
]


def add_production_services():
    with Session(engine) as session:
        inserted = 0
        skipped = 0

        for item in PRODUCTION_SERVICES:
            existing = session.scalar(
                select(HealthcareService).where(
                    HealthcareService.service_code == item["service_code"]
                )
            )

            if existing is None:
                session.add(HealthcareService(**item))
                inserted += 1
            else:
                skipped += 1

        session.commit()

        print("Production service categories processed.")
        print("New categories inserted:", inserted)
        print("Existing categories skipped:", skipped)


if __name__ == "__main__":
    add_production_services()
    engine.dispose()


from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import engine
from src.models import Base, Facility, HealthcareService, FacilityService


# These are fictional records for software testing only.
# They do not represent real Bengaluru hospitals or their services.

TEST_FACILITIES = [
    {
        "name": "TEST ONLY - Bengaluru Facility A",
        "city": "Bengaluru",
        "address": "Fictional address A",
    },
    {
        "name": "TEST ONLY - Bengaluru Facility B",
        "city": "Bengaluru",
        "address": "Fictional address B",
    },
    {
        "name": "TEST ONLY - Bengaluru Facility C",
        "city": "Bengaluru",
        "address": "Fictional address C",
    },
]

TEST_SERVICES = [
    {
        "service_code": "TEST_CHEMO",
        "service_name": "Chemotherapy",
        "description": "Test service record; not verified facility information.",
    },
    {
        "service_code": "TEST_RADIATION",
        "service_name": "Radiation Therapy",
        "description": "Test service record; not verified facility information.",
    },
    {
        "service_code": "TEST_SURGERY",
        "service_name": "Cancer Surgery",
        "description": "Test service record; not verified facility information.",
    },
    {
        "service_code": "TEST_IMMUNOTHERAPY",
        "service_name": "Immunotherapy",
        "description": "Test service record; not verified facility information.",
    },
]


# Fictional service combinations used to test database relationships.
TEST_MAPPINGS = {
    "TEST ONLY - Bengaluru Facility A": [
        "TEST_CHEMO",
        "TEST_RADIATION",
    ],
    "TEST ONLY - Bengaluru Facility B": [
        "TEST_CHEMO",
        "TEST_SURGERY",
        "TEST_IMMUNOTHERAPY",
    ],
    "TEST ONLY - Bengaluru Facility C": [
        "TEST_RADIATION",
        "TEST_SURGERY",
    ],
}


def seed_database():
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        # Insert facilities without duplicating existing test records.
        for item in TEST_FACILITIES:
            existing = session.scalar(
                select(Facility).where(Facility.name == item["name"])
            )
            if existing is None:
                session.add(
                    Facility(
                        **item,
                        verification_source="Synthetic test data only",
                    )
                )

        # Insert services without duplicating service codes.
        for item in TEST_SERVICES:
            existing = session.scalar(
                select(HealthcareService).where(
                    HealthcareService.service_code
                    == item["service_code"]
                )
            )
            if existing is None:
                session.add(HealthcareService(**item))

        session.flush()

        # Create facility-service links, all explicitly unverified.
        for facility_name, service_codes in TEST_MAPPINGS.items():
            facility = session.scalar(
                select(Facility).where(Facility.name == facility_name)
            )

            for service_code in service_codes:
                service = session.scalar(
                    select(HealthcareService).where(
                        HealthcareService.service_code == service_code
                    )
                )

                existing_link = session.scalar(
                    select(FacilityService).where(
                        FacilityService.facility_id == facility.facility_id,
                        FacilityService.service_id == service.service_id,
                    )
                )

                if existing_link is None:
                    session.add(
                        FacilityService(
                            facility_id=facility.facility_id,
                            service_id=service.service_id,
                            is_verified=False,
                            verification_source="Synthetic test mapping only",
                        )
                    )

        session.commit()

        print("Test data inserted successfully!")
        print("Facilities:", session.query(Facility).count())
        print("Healthcare services:", session.query(HealthcareService).count())
        print("Facility-service links:", session.query(FacilityService).count())


if __name__ == "__main__":
    try:
        seed_database()
    except Exception as error:
        print("Seeding failed:", type(error).__name__, error)
    finally:
        engine.dispose()


from app.database import Base, engine, SessionLocal
from app.models import Facility


SAMPLE_FACILITIES = [
    {
        "facility_name": "Sample Cancer Care Centre",
        "city": "Bengaluru",
        "cancer_types": ["Breast", "Lung"],
        "services": [
            "Chemotherapy",
            "Radiation Therapy",
            "Surgery",
            "Immunotherapy",
        ],
        "address": "Sample Address, Bengaluru",
        "contact_number": None,
        "facility_type": "Cancer Care Centre",
    },
    {
        "facility_name": "Sample Oncology Hospital",
        "city": "Mysuru",
        "cancer_types": ["Breast", "Lung"],
        "services": ["Chemotherapy", "Surgery"],
        "address": "Sample Address, Mysuru",
        "contact_number": None,
        "facility_type": "Hospital",
    },
]


def initialize_database():
    # Create missing tables without dropping existing tables.
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        for facility_data in SAMPLE_FACILITIES:
            existing_facility = (
                db.query(Facility)
                .filter_by(
                    facility_name=facility_data["facility_name"],
                    city=facility_data["city"],
                )
                .first()
            )

            if existing_facility is None:
                db.add(Facility(**facility_data))

        db.commit()
        print("Database initialization completed successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    initialize_database()

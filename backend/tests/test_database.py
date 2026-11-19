
from sqlalchemy import text

from app.database import engine, SessionLocal
from app.models import Facility
from app.init_db import initialize_database


def test_database_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1")).scalar()

    assert result == 1


def test_facility_table_is_accessible():
    with SessionLocal() as db:
        facilities = db.query(Facility).all()

    assert facilities is not None


def test_existing_sample_facilities():
    with SessionLocal() as db:
        names = [
            facility.facility_name
            for facility in db.query(Facility).all()
        ]

    assert "Sample Cancer Care Centre" in names
    assert "Sample Oncology Hospital" in names


def test_initialization_does_not_create_duplicates():
    with SessionLocal() as db:
        count_before = db.query(Facility).count()

    initialize_database()

    with SessionLocal() as db:
        count_after = db.query(Facility).count()

    assert count_after == count_before

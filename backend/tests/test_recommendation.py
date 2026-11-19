
import pytest

from app.database import SessionLocal
from app.models import Facility
from app.recommendation import recommend_facilities


def test_bengaluru_facility_filtering():
    with SessionLocal() as db:
        results = recommend_facilities(
            db,
            city="Bengaluru",
            cancer_type="Breast Cancer"
        )

    assert len(results) == 1
    assert results[0]["facility_name"] == "Sample Cancer Care Centre"


def test_mysuru_facility_filtering():
    with SessionLocal() as db:
        results = recommend_facilities(
            db,
            city="Mysuru",
            cancer_type="Lung Cancer"
        )

    assert len(results) == 1
    assert results[0]["facility_name"] == "Sample Oncology Hospital"


def test_city_filter_is_case_insensitive():
    with SessionLocal() as db:
        results = recommend_facilities(
            db,
            city="bengaluru",
            cancer_type="Breast Cancer"
        )

    assert len(results) == 1
    assert results[0]["city"] == "Bengaluru"


def test_unsupported_city_returns_empty_list():
    with SessionLocal() as db:
        results = recommend_facilities(
            db,
            city="Chennai",
            cancer_type="Breast Cancer"
        )

    assert results == []


def test_invalid_cancer_type_is_rejected():
    with SessionLocal() as db:
        with pytest.raises(ValueError):
            recommend_facilities(
                db,
                city="Bengaluru",
                cancer_type="Other Cancer"
            )


def test_existing_facilities_do_not_claim_unverified_support():
    with SessionLocal() as db:
        results = recommend_facilities(
            db,
            city="Bengaluru",
            cancer_type="Breast Cancer",
            required_support_services=["Psychological support"]
        )

    assert len(results) == 1
    assert results[0]["matched_support_services"] == []
    assert results[0]["unmatched_support_services"] == [
        "Psychological support"
    ]
    assert results[0]["match_score"] == 0


def test_verified_support_services_are_matched_and_ranked():
    with SessionLocal() as db:
        try:
            facility_one = Facility(
                facility_name="Test Facility One",
                city="Test City",
                cancer_types=["Breast"],
                services=[],
                support_services=["Psychological support"],
                address="Test Address One"
            )

            facility_two = Facility(
                facility_name="Test Facility Two",
                city="Test City",
                cancer_types=["Breast"],
                services=[],
                support_services=[
                    "Psychological support",
                    "Nutrition support"
                ],
                address="Test Address Two"
            )

            db.add_all([facility_one, facility_two])
            db.flush()

            results = recommend_facilities(
                db,
                city="Test City",
                cancer_type="Breast Cancer",
                required_support_services=[
                    "Psychological support",
                    "Nutrition support"
                ]
            )

            assert len(results) == 2
            assert results[0]["facility_name"] == "Test Facility Two"
            assert results[0]["match_score"] == 2
            assert results[1]["facility_name"] == "Test Facility One"
            assert results[1]["match_score"] == 1

        finally:
            # Test records are not permanently stored.
            db.rollback()


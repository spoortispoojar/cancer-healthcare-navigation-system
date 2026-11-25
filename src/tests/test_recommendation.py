
from types import SimpleNamespace

import src.recommendation as recommendation


class FakeSession:
    """Mock database session for testing without PostgreSQL."""

    def __init__(self, facilities):
        self.facilities = facilities

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def scalars(self, statement):
        return FakeScalarResult(self.facilities)


class FakeScalarResult:
    def __init__(self, facilities):
        self.facilities = facilities

    def unique(self):
        return self

    def all(self):
        return self.facilities

def create_facility(
    name,
    services,
    latitude=None,
    longitude=None,
):
    """Create a simulated hospital with its services."""

    mappings = []

    for code, service_name, verified in services:
        service = SimpleNamespace(
            service_code=code,
            service_name=service_name,
        )

        mappings.append(
            SimpleNamespace(
                service=service,
                is_verified=verified,
            )
        )

    return SimpleNamespace(
        facility_id=1,
        name=name,
        city="Bengaluru",
        latitude=latitude,
        longitude=longitude,
        services=mappings,
    )
def mock_database(monkeypatch, facilities):
    monkeypatch.setattr(
        recommendation,
        "Session",
        lambda engine: FakeSession(facilities),
    )


def test_empty_required_services():
    result = recommendation.recommend_facilities(
        required_service_codes=[],
        city="Bengaluru",
    )

    assert result["status"] == "NO_REQUIRED_SERVICES"
    assert result["results"] == []


def test_invalid_city():
    result = recommendation.recommend_facilities(
        required_service_codes=["TEST_CHEMO"],
        city="",
    )

    assert result["status"] == "INVALID_CITY"
    assert result["results"] == []


def test_verified_service_matching(monkeypatch):
    facility = create_facility(
        "Test Hospital A",
        [
            ("TEST_CHEMO", "Chemotherapy", True),
        ],
    )

    mock_database(monkeypatch, [facility])

    result = recommendation.recommend_facilities(
        required_service_codes=["TEST_CHEMO"],
        city="Bengaluru",
    )

    hospital = result["results"][0]

    assert hospital["match_percentage"] == 100.0
    assert hospital["matched_services"] == ["Chemotherapy"]
    assert hospital["unmatched_service_codes"] == []
    assert hospital["verification_status"] == "VERIFIED SERVICE MATCHES"


def test_missing_required_services(monkeypatch):
    facility = create_facility(
        "Test Hospital B",
        [
            ("TEST_CHEMO", "Chemotherapy", True),
        ],
    )

    mock_database(monkeypatch, [facility])

    result = recommendation.recommend_facilities(
        required_service_codes=[
            "TEST_CHEMO",
            "TEST_RADIATION",
        ],
        city="Bengaluru",
    )

    hospital = result["results"][0]

    assert hospital["match_count"] == 1
    assert hospital["required_count"] == 2
    assert hospital["match_percentage"] == 50.0
    assert hospital["unmatched_service_codes"] == ["TEST_RADIATION"]


def test_unverified_service_excluded_by_default(monkeypatch):
    facility = create_facility(
        "Test Hospital C",
        [
            ("TEST_CHEMO", "Chemotherapy", False),
        ],
    )

    mock_database(monkeypatch, [facility])

    result = recommendation.recommend_facilities(
        required_service_codes=["TEST_CHEMO"],
        city="Bengaluru",
    )

    hospital = result["results"][0]

    assert hospital["match_percentage"] == 0.0
    assert hospital["matched_services"] == []


def test_unverified_service_included_in_test_mode(monkeypatch):
    facility = create_facility(
        "Test Hospital D",
        [
            ("TEST_CHEMO", "Chemotherapy", False),
        ],
    )

    mock_database(monkeypatch, [facility])

    result = recommendation.recommend_facilities(
        required_service_codes=["TEST_CHEMO"],
        city="Bengaluru",
        include_unverified_for_testing=True,
    )

    hospital = result["results"][0]

    assert hospital["match_percentage"] == 100.0
    assert hospital["verification_status"] == "UNVERIFIED TEST DATA"


def test_hospitals_ranked_by_service_coverage(monkeypatch):
    hospital_a = create_facility(
        "Hospital A",
        [
            ("TEST_CHEMO", "Chemotherapy", True),
        ],
    )

    hospital_b = create_facility(
        "Hospital B",
        [
            ("TEST_CHEMO", "Chemotherapy", True),
            ("TEST_RAD", "Radiation Therapy", True),
        ],
    )

    mock_database(monkeypatch, [hospital_a, hospital_b])

    result = recommendation.recommend_facilities(
        required_service_codes=[
            "TEST_CHEMO",
            "TEST_RAD",
        ],
        city="Bengaluru",
    )

    hospitals = result["results"]

    assert hospitals[0]["facility_name"] == "Hospital B"
    assert hospitals[0]["match_percentage"] == 100.0

    assert hospitals[1]["facility_name"] == "Hospital A"
    assert hospitals[1]["match_percentage"] == 50.0

def test_invalid_service_codes():
    result = recommendation.recommend_facilities(
        required_service_codes=["", None, 123],
        city="Bengaluru",
    )

    assert result["status"] == "NO_REQUIRED_SERVICES"
    assert result["results"] == []


def test_no_matching_services(monkeypatch):
    facility = create_facility(
        "Test Hospital E",
        [
            ("TEST_SURGERY", "Surgery", True),
        ],
    )

    mock_database(monkeypatch, [facility])

    result = recommendation.recommend_facilities(
        required_service_codes=["TEST_CHEMO"],
        city="Bengaluru",
    )

    hospital = result["results"][0]

    assert hospital["match_count"] == 0
    assert hospital["match_percentage"] == 0.0
    assert hospital["unmatched_service_codes"] == ["TEST_CHEMO"]


def test_service_code_case_insensitive(monkeypatch):
    facility = create_facility(
        "Test Hospital F",
        [
            ("test_chemo", "Chemotherapy", True),
        ],
    )

    mock_database(monkeypatch, [facility])

    result = recommendation.recommend_facilities(
        required_service_codes=[" test_chemo "],
        city="Bengaluru",
    )

    assert result["results"][0]["match_percentage"] == 100.0


def test_equal_match_percentage_sorted_alphabetically(monkeypatch):
    hospital_a = create_facility(
        "Apollo Test Hospital",
        [("TEST_CHEMO", "Chemotherapy", True)],
    )

    hospital_b = create_facility(
        "City Test Hospital",
        [("TEST_CHEMO", "Chemotherapy", True)],
    )

    mock_database(monkeypatch, [hospital_a, hospital_b])

    result = recommendation.recommend_facilities(
        required_service_codes=["TEST_CHEMO"],
        city="Bengaluru",
    )

    hospitals = result["results"]

    assert hospitals[0]["facility_name"] == "Apollo Test Hospital"
    assert hospitals[1]["facility_name"] == "City Test Hospital"
from src.recommendation import normalize_service_code


def test_radiation_service_codes_remain_separate():
    assert normalize_service_code("RADIATION_ONCOLOGY") == "RADIATION_ONCOLOGY"
    assert normalize_service_code("RADIATION") == "RADIATION"


def test_closer_hospital_ranks_first_when_service_match_is_equal(monkeypatch):
    nearby = create_facility(
        "Nearby Hospital",
        [("TEST_CHEMO", "Chemotherapy", True)],
        latitude=12.9800,
        longitude=77.5900,
    )

    farther = create_facility(
        "Farther Hospital",
        [("TEST_CHEMO", "Chemotherapy", True)],
        latitude=13.1000,
        longitude=77.5900,
    )

    mock_database(monkeypatch, [farther, nearby])

    result = recommendation.recommend_facilities(
        required_service_codes=["TEST_CHEMO"],
        city="Bengaluru",
        patient_latitude=12.9716,
        patient_longitude=77.5946,
    )

    hospitals = result["results"]

    assert hospitals[0]["facility_name"] == "Nearby Hospital"
    assert hospitals[1]["facility_name"] == "Farther Hospital"
    assert hospitals[0]["distance_km"] < hospitals[1]["distance_km"]


def test_service_coverage_has_priority_over_distance(monkeypatch):
    farther_full_match = create_facility(
        "Farther Full Match Hospital",
        [
            ("TEST_CHEMO", "Chemotherapy", True),
            ("TEST_RAD", "Radiation Therapy", True),
        ],
        latitude=13.1000,
        longitude=77.5900,
    )

    nearby_partial_match = create_facility(
        "Nearby Partial Match Hospital",
        [("TEST_CHEMO", "Chemotherapy", True)],
        latitude=12.9800,
        longitude=77.5900,
    )

    mock_database(
        monkeypatch,
        [nearby_partial_match, farther_full_match],
    )

    result = recommendation.recommend_facilities(
        required_service_codes=["TEST_CHEMO", "TEST_RAD"],
        city="Bengaluru",
        patient_latitude=12.9716,
        patient_longitude=77.5946,
    )

    hospitals = result["results"]

    assert hospitals[0]["facility_name"] == "Farther Full Match Hospital"
    assert hospitals[0]["match_percentage"] == 100.0
    assert hospitals[1]["match_percentage"] == 50.0


def test_missing_facility_coordinates_return_none(monkeypatch):
    facility = create_facility(
        "Hospital Without Coordinates",
        [("TEST_CHEMO", "Chemotherapy", True)],
    )

    mock_database(monkeypatch, [facility])

    result = recommendation.recommend_facilities(
        required_service_codes=["TEST_CHEMO"],
        city="Bengaluru",
        patient_latitude=12.9716,
        patient_longitude=77.5946,
    )

    assert len(result["results"]) == 1
    assert result["results"][0]["distance_km"] is None


def test_partial_patient_coordinates_are_rejected(monkeypatch):
    result = recommendation.recommend_facilities(
        required_service_codes=["TEST_CHEMO"],
        city="Bengaluru",
        patient_latitude=12.9716,
    )

    assert result["status"] == "INVALID_COORDINATES"
    assert result["results"] == []


"""
Facility recommendation and ranking module.

Ranks facilities by required-service match percentage,
then by distance when patient coordinates are available.

This is a healthcare navigation support feature,
not a clinical recommendation.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from src.database import engine
from src.models import Facility, FacilityService
from src.distance import calculate_distance_km


def normalize_service_code(code):
    """Normalize service codes."""
    return code.strip().upper()


def recommend_facilities(
    required_service_codes,
    city,
    include_unverified_for_testing=False,
    patient_latitude=None,
    patient_longitude=None,
):
    """Recommend facilities using service coverage and distance."""

    if not required_service_codes:
        return {
            "status": "NO_REQUIRED_SERVICES",
            "results": [],
            "message": "No required service codes were provided.",
        }

    required_codes = {
        normalize_service_code(code)
        for code in required_service_codes
        if isinstance(code, str) and code.strip()
    }

    if not required_codes:
        return {
            "status": "NO_REQUIRED_SERVICES",
            "results": [],
            "message": "No valid service codes were provided.",
        }

    if not isinstance(city, str) or not city.strip():
        return {
            "status": "INVALID_CITY",
            "results": [],
            "message": "Please provide a valid city.",
        }

    # Patient coordinates must be supplied together.
    if (patient_latitude is None) != (patient_longitude is None):
        return {
            "status": "INVALID_COORDINATES",
            "results": [],
            "message": "Provide both patient latitude and longitude.",
        }

    # Validate patient coordinates before querying facilities.
    if patient_latitude is not None:
        try:
            calculate_distance_km(
                patient_latitude,
                patient_longitude,
                patient_latitude,
                patient_longitude,
            )
        except (ValueError, TypeError):
            return {
                "status": "INVALID_COORDINATES",
                "results": [],
                "message": "Patient coordinates are invalid.",
            }

    with Session(engine) as session:
        statement = (
            select(Facility)
            .where(Facility.city.ilike(city.strip()))
            .options(
                selectinload(Facility.services).selectinload(
                    FacilityService.service
                )
            )
        )

        facilities = session.scalars(statement).unique().all()
        results = []

        for facility in facilities:
            matched_services = {}
            unverified_services = set()

            for mapping in facility.services:
                service = mapping.service

                if service is None:
                    continue

                service_code = normalize_service_code(
                    service.service_code
                )

                if service_code not in required_codes:
                    continue

                if not mapping.is_verified:
                    if not include_unverified_for_testing:
                        continue

                    unverified_services.add(service_code)

                matched_services[service_code] = service.service_name

            matched_codes = set(matched_services)
            match_count = len(matched_codes)
            required_count = len(required_codes)

            match_percentage = round(
                match_count / required_count * 100, 2
            )

            if unverified_services:
                verification_status = "UNVERIFIED TEST DATA"
            elif matched_codes:
                verification_status = "VERIFIED SERVICE MATCHES"
            else:
                verification_status = "NO VERIFIED SERVICE MATCH"

            # Calculate distance only when both coordinate pairs exist.
            distance_km = None

            if (
                patient_latitude is not None
                and facility.latitude is not None
                and facility.longitude is not None
            ):
                distance_km = calculate_distance_km(
                    patient_latitude,
                    patient_longitude,
                    facility.latitude,
                    facility.longitude,
                )

            results.append(
                {
                    "facility_id": facility.facility_id,
                    "facility_name": facility.name,
                    "city": facility.city,
                    "matched_services": list(
                        matched_services.values()
                    ),
                    "match_count": match_count,
                    "required_count": required_count,
                    "match_percentage": match_percentage,
                    "unmatched_service_codes": sorted(
                        required_codes - matched_codes
                    ),
                    "verification_status": verification_status,
                    "distance_km": distance_km,
                }
            )

        # Highest service coverage first.
        # Shortest known distance breaks equal-coverage ties.
        # Missing distances come after known distances.
        # Hospital name provides the final alphabetical tie-break.
        results.sort(
            key=lambda item: (
                -item["match_percentage"],
                item["distance_km"] is None,
                (
                    item["distance_km"]
                    if item["distance_km"] is not None
                    else float("inf")
                ),
                item["facility_name"].lower(),
            )
        )

    return {
        "status": (
            "TEST_ONLY_UNVERIFIED"
            if include_unverified_for_testing
            else "VERIFIED_ONLY"
        ),
        "results": results,
        "message": (
            "Ranking is based on required-service coverage, "
            "followed by distance when available. "
            "It does not measure clinical quality or treatment success."
        ),
    }


if __name__ == "__main__":
    test_requirements = ["TEST_CHEMO"]

    output = recommend_facilities(
        required_service_codes=test_requirements,
        city="Bengaluru",
        include_unverified_for_testing=True,
        patient_latitude=12.9716,
        patient_longitude=77.5946,
    )

    print("\nFacility Recommendation Test")
    print("============================")
    print("Status:", output["status"])
    print("Message:", output["message"])

    for item in output["results"]:
        print("\nFacility:", item["facility_name"])
        print("Match:", f'{item["match_percentage"]}%')
        print("Distance:", item["distance_km"], "km")
        print("Services:", item["matched_services"])
        print("Verification:", item["verification_status"])

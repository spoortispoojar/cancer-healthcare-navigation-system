
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Facility


# Map frontend/ML cancer labels to database labels.
CANCER_TYPE_MAP = {
    "Breast Cancer": "Breast",
    "Lung Cancer": "Lung",
}


def recommend_facilities(
    db: Session,
    city: str,
    cancer_type: str,
    required_support_services: list[str] | None = None
) -> list[dict]:
    """
    Find and rank facilities using location, cancer type,
    and verified available support services.

    Facilities are ranked by the number of requested support
    services they explicitly list as available.

    A facility can still match by city and cancer type when
    no requested support services are listed.
    """

    if not isinstance(city, str) or not city.strip():
        raise ValueError("A valid city is required.")

    if cancer_type not in CANCER_TYPE_MAP:
        raise ValueError(
            "Cancer type must be Breast Cancer or Lung Cancer."
        )

    if required_support_services is None:
        required_support_services = []

    if not isinstance(required_support_services, list):
        raise TypeError(
            "Required support services must be a list."
        )

    if any(
        not isinstance(service, str) or not service.strip()
        for service in required_support_services
    ):
        raise ValueError(
            "Every requested support service must be a non-empty string."
        )

    database_cancer_type = CANCER_TYPE_MAP[cancer_type]

    # Find facilities in the requested city.
    city_facilities = (
        db.query(Facility)
        .filter(
            func.lower(Facility.city) == city.strip().lower()
        )
        .all()
    )

    recommendations = []

    for facility in city_facilities:

        # Check whether the facility supports this cancer type.
        supported_cancer_types = {
            item.casefold()
            for item in (facility.cancer_types or [])
        }

        if database_cancer_type.casefold() not in supported_cancer_types:
            continue

        # Only use explicitly recorded support services.
        available_support_services = (
            facility.support_services or []
        )

        available_lookup = {
            service.casefold(): service
            for service in available_support_services
        }

        matched_services = [
            available_lookup[service.casefold()]
            for service in required_support_services
            if service.casefold() in available_lookup
        ]

        unmatched_services = [
            service
            for service in required_support_services
            if service.casefold() not in available_lookup
        ]

        # Transparent ranking: one point per matched support service.
        match_score = len(matched_services)

        explanation = [
            f"Located in {facility.city}.",
            f"Lists support for {database_cancer_type} cancer."
        ]

        if matched_services:
            explanation.append(
                "Verified matching support services: "
                + ", ".join(matched_services)
                + "."
            )

        elif required_support_services:
            explanation.append(
                "No requested support services are currently "
                "listed as verified for this facility."
            )

        else:
            explanation.append(
                "No additional support services were requested."
            )

        recommendations.append({
            "facility_id": facility.id,
            "facility_name": facility.facility_name,
            "city": facility.city,
            "address": facility.address,
            "contact_number": facility.contact_number,
            "facility_type": facility.facility_type,
            "cancer_types": facility.cancer_types,
            "services": facility.services,
            "support_services": available_support_services,
            "matched_support_services": matched_services,
            "unmatched_support_services": unmatched_services,
            "match_score": match_score,
            "match_explanation": " ".join(explanation)
        })

    # Highest support-service match first.
    # Facility name provides deterministic ordering for ties.
    recommendations.sort(
        key=lambda item: (
            -item["match_score"],
            item["facility_name"].casefold()
        )
    )

    return recommendations

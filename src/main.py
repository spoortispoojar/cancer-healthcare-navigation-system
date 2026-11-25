
"""
Main workflow for the cancer healthcare navigation project.

This is a software test, not a diagnosis or clinical recommendation.
"""

from src.requirement_mapping import map_requirements
from src.recommendation import recommend_facilities


def run_workflow(patient_profile):
    print("\n========== PATIENT PROFILE ==========")
    print("Cancer type:", patient_profile["cancer_type"])
    print("Current treatment:", patient_profile["current_treatment"])
    print("City:", patient_profile["city"])

    # Step 1: Map the stated treatment to required service codes.
    mapping_result = map_requirements(patient_profile)

    print("\n========== REQUIREMENT MAPPING ==========")
    print("Required services:", mapping_result["required_services"])
    print("Mapping message:", mapping_result["message"])

    required_services = mapping_result["required_services"]

    if not required_services:
        print("\nNo recommendations generated.")
        print("Reason:", mapping_result["message"])
        return

    # Step 2: Rank facilities using the required service codes.
    recommendation_result = recommend_facilities(
        required_service_codes=required_services,
        city=patient_profile["city"],
    )

    print("\n========== FACILITY RESULTS ==========")
    print("Result status:", recommendation_result["status"])
    print("Explanation:", recommendation_result["message"])

    if not recommendation_result["results"]:
        print("No facilities found for this city.")
        return

    for rank, facility in enumerate(
        recommendation_result["results"], start=1
    ):
        print(f"\nRank: {rank}")
        print("Facility:", facility["facility_name"])
        print("Service match:", f'{facility["match_percentage"]}%')
        print("Matched services:", facility["matched_services"])
        print("Unmatched services:", facility["unmatched_service_codes"])
        print("Verification:", facility["verification_status"])

    print("\nIMPORTANT:")
    print("These results use synthetic, unverified test data.")
    print("They are not real hospital recommendations.")
    print("The percentage measures service overlap only.")


if __name__ == "__main__":
    sample_patient = {
        "cancer_type": "Breast",
        "current_treatment": "Chemo",
        "symptoms": ["fatigue"],
        "severity": "moderate",
        "duration": "2 weeks",
        "city": "Bengaluru",
        "support_level": "Moderate",
    }

    run_workflow(sample_patient)

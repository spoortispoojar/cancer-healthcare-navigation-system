
from fastapi import APIRouter, HTTPException, Query

from app.schemas import PatientAssessment, StructuredPatientProfile
from app.recommendation import find_facilities

router = APIRouter()


@router.post("/assessment/profile", response_model=StructuredPatientProfile)
def create_patient_profile(assessment: PatientAssessment):
    return StructuredPatientProfile(
        cancer_type=assessment.cancer_type,
        current_treatment=assessment.current_treatment,
        symptoms=assessment.symptoms,
        severity=assessment.severity,
        duration_days=assessment.duration_days,
        city=assessment.city.strip(),
    )


@router.get("/facilities")
def get_facilities(
    city: str = Query(min_length=2, max_length=100),
    cancer_type: str = Query(),
    current_treatment: str = Query(),
):
    if cancer_type not in ["Breast", "Lung"]:
        raise HTTPException(
            status_code=422,
            detail="cancer_type must be Breast or Lung",
        )

    allowed_treatments = [
        "Chemotherapy",
        "Radiation Therapy",
        "Surgery",
        "Immunotherapy",
        "Other",
    ]

    if current_treatment not in allowed_treatments:
        raise HTTPException(
            status_code=422,
            detail="Invalid current_treatment",
        )

    try:
        facilities = find_facilities(
            city,
            cancer_type,
            current_treatment,
        )
        return {
            "city": city.strip(),
            "cancer_type": cancer_type,
            "current_treatment": current_treatment,
            "count": len(facilities),
            "facilities": facilities,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve facilities from the database",
        ) from exc


@router.post("/assessment/recommendations")
def get_assessment_recommendations(assessment: PatientAssessment):
    profile = create_patient_profile(assessment)

    try:
        facilities = find_facilities(
            profile.city,
            profile.cancer_type,
            profile.current_treatment,
        )

        for facility in facilities:
            facility["match_reason"] = (
                f"Located in {facility['city']}; "
                f"supports {profile.cancer_type} cancer care "
                f"and lists {profile.current_treatment} as a service."
            )

        return {
            "patient_profile": profile.model_dump(),
            "facility_count": len(facilities),
            "facilities": facilities,
            "message": (
                "Facility matches retrieved successfully."
                if facilities
                else "No matching facilities found for this city, cancer type, and treatment."
            ),
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve facility recommendations",
        ) from exc

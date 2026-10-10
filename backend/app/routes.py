
from fastapi import APIRouter

from app.schemas import (
    PatientAssessment,
    StructuredPatientProfile,
)

router = APIRouter()


@router.post("/assessment/profile", response_model=StructuredPatientProfile)
def create_patient_profile(
    assessment: PatientAssessment,
):
    profile = StructuredPatientProfile(
        cancer_type=assessment.cancer_type,
        current_treatment=assessment.current_treatment,
        symptoms=assessment.symptoms,
        severity=assessment.severity,
        duration_days=assessment.duration_days,
        city=assessment.city.strip(),
    )

    return profile

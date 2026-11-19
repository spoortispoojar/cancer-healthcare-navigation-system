
from typing import Callable

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import AssessmentRequest
from app.service_mapping import map_support_services
from app.recommendation import recommend_facilities


router = APIRouter()



def get_support_predictor():
    """
    The real ML predictor will be connected in Phase 9.
    No fabricated prediction is returned.
    """

    def unavailable_predictor(patient_data):
        raise HTTPException(
            status_code=503,
            detail="ML model integration is not yet available."
        )

    return unavailable_predictor



@router.post("/assessment")
def create_assessment(
    request: AssessmentRequest,
    db: Session = Depends(get_db),
    predictor: Callable[[dict], dict] = Depends(get_support_predictor)
):
    # 1. Convert validated patient input into the exact
    #    35 feature names expected by the ML model.
    patient_data = request.patient.model_dump(by_alias=True)

    # 2. Obtain the ML prediction.
    prediction = predictor(patient_data)

    if not isinstance(prediction, dict):
        raise HTTPException(
            status_code=500,
            detail="Invalid ML prediction response."
        )

    support_requirement = prediction.get("support_requirement")

    if support_requirement not in {"Low", "Moderate", "High"}:
        raise HTTPException(
            status_code=500,
            detail="Invalid support requirement returned by the predictor."
        )

    # 3. Map relevant healthcare support services.
    support_result = map_support_services(
        patient_data,
        support_requirement
    )

    required_services = [
        item["service"]
        for item in support_result["services"]
    ]

    # 4. Find suitable facilities.
    facilities = recommend_facilities(
        db=db,
        city=request.city,
        cancer_type=patient_data["cancer_type"],
        required_support_services=required_services
    )

    # 5. Return a structured response.
    return {
        "status": "success",
        "patient_summary": {
            "cancer_type": patient_data["cancer_type"],
            "city": request.city
        },
        "support_requirement": support_requirement,
        "coordination_guidance": support_result[
            "coordination_guidance"
        ],
        "support_services": support_result["services"],
        "recommended_facilities": facilities,
        "message": (
            "Healthcare navigation recommendations "
            "generated successfully."
        ),
        "disclaimer": support_result["disclaimer"]
    }

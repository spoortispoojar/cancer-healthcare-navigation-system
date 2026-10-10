
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class PatientAssessment(BaseModel):
    cancer_type: Literal["Breast", "Lung"]

    current_treatment: Literal[
        "Chemotherapy",
        "Radiation Therapy",
        "Surgery",
        "Immunotherapy",
        "Other",
    ]

    symptoms: list[
        Literal[
            "Pain",
            "Vomiting",
            "Weakness",
            "Fever",
            "Breathlessness",
            "Cough",
            "Fatigue",
            "Other",
        ]
    ] = Field(min_length=1)

    severity: Literal["Mild", "Moderate", "Severe"]
    duration_days: int = Field(ge=0, le=36500)
    city: str = Field(min_length=2, max_length=100)

    @field_validator("city")
    @classmethod
    def clean_city(cls, value: str) -> str:
        value = value.strip()

        if len(value) < 2:
            raise ValueError("City must contain at least 2 characters")

        return value


class StructuredPatientProfile(BaseModel):
    cancer_type: str
    current_treatment: str
    symptoms: list[str]
    severity: str
    duration_days: int
    city: str

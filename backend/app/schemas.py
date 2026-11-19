
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictInt,
    field_validator
)


class PatientMLInput(BaseModel):
    """
    Validates the 35 features required by the ML model.
    Feature names and categorical values must match
    the ML training dataset.
    """

    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True
    )
    @field_validator("age_years", mode="before")
    @classmethod
    def reject_boolean_age(cls, value):
        if isinstance(value, bool):
            raise ValueError("Age must be a valid positive number.")

        return value
    # --------------------------------
    # 1. Numerical feature
    # --------------------------------

    age_years: float = Field(gt=0)

    # --------------------------------
    # 2. Categorical features
    # --------------------------------

    cancer_type: Literal[
        "Breast Cancer",
        "Lung Cancer"
    ]

    cancer_stage: Literal[
        "Not sure",
        "Stage I",
        "Stage II",
        "Stage III",
        "Stage IV"
    ]

    current_treatment: Literal[
        "Chemoradiation",
        "Chemotherapy",
        "Chemotherapy + Immunotherapy",
        "Chemotherapy + Radiation therapy",
        "Chemotherapy + Targeted therapy",
        "Follow-up only (treatment completed)",
        "Hormone therapy",
        "Immunotherapy",
        "Not started yet (newly diagnosed)",
        "Palliative / supportive care",
        "Radiation therapy",
        "Surgery (lobectomy or segmentectomy)",
        "Surgery (lumpectomy)",
        "Surgery (mastectomy)",
        "Targeted therapy (EGFR/ALK)",
        "Targeted therapy (HER2)"
    ]

    symptom_severity: Literal[
        "Mild",
        "Moderate",
        "None reported",
        "Severe"
    ]

    symptom_duration: Literal[
        "1-3 months",
        "1-4 weeks",
        "3-6 months",
        "Less than 1 week",
        "More than 6 months",
        "Not applicable"
    ]

    symptom_frequency: Literal[
        "Constant",
        "Daily",
        "Not applicable",
        "Occasionally",
        "Several times a week"
    ]

    needs_caregiver_support: Literal[
        "No",
        "Sometimes",
        "Yes"
    ]

    has_transport_to_hospital: Literal[
        "No",
        "Sometimes",
        "Yes"
    ]

    # --------------------------------
    # 3. Binary symptom features
    # --------------------------------

    fatigue: StrictInt = Field(alias="Fatigue", ge=0, le=1)

    shortness_of_breath: StrictInt = Field(
        alias="Shortness of breath", ge=0, le=1
    )

    nausea: StrictInt = Field(alias="Nausea", ge=0, le=1)

    bone_pain: StrictInt = Field(alias="Bone pain", ge=0, le=1)

    weight_loss: StrictInt = Field(alias="Weight loss", ge=0, le=1)

    anxiety_or_low_mood: StrictInt = Field(
        alias="Anxiety or low mood", ge=0, le=1
    )

    loss_of_appetite: StrictInt = Field(
        alias="Loss of appetite", ge=0, le=1
    )

    persistent_cough: StrictInt = Field(
        alias="Persistent cough", ge=0, le=1
    )

    sleep_difficulty: StrictInt = Field(
        alias="Sleep difficulty", ge=0, le=1
    )

    breast_lump: StrictInt = Field(
        alias="Breast lump", ge=0, le=1
    )

    breast_pain: StrictInt = Field(
        alias="Breast pain", ge=0, le=1
    )

    chest_pain: StrictInt = Field(
        alias="Chest pain", ge=0, le=1
    )

    tingling_or_numbness: StrictInt = Field(
        alias="Tingling or numbness in hands/feet",
        ge=0,
        le=1
    )

    shoulder_stiffness: StrictInt = Field(
        alias="Shoulder stiffness", ge=0, le=1
    )

    arm_swelling: StrictInt = Field(
        alias="Arm swelling (lymphedema)", ge=0, le=1
    )

    skin_changes_or_redness: StrictInt = Field(
        alias="Skin changes or redness", ge=0, le=1
    )

    hair_loss: StrictInt = Field(
        alias="Hair loss", ge=0, le=1
    )

    coughing_up_blood: StrictInt = Field(
        alias="Coughing up blood", ge=0, le=1
    )

    wheezing: StrictInt = Field(
        alias="Wheezing", ge=0, le=1
    )

    recurrent_chest_infections: StrictInt = Field(
        alias="Recurrent chest infections", ge=0, le=1
    )

    hot_flashes: StrictInt = Field(
        alias="Hot flashes", ge=0, le=1
    )

    hoarseness: StrictInt = Field(
        alias="Hoarseness", ge=0, le=1
    )

    difficulty_swallowing: StrictInt = Field(
        alias="Difficulty swallowing", ge=0, le=1
    )

    skin_rash: StrictInt = Field(
        alias="Skin rash", ge=0, le=1
    )

    nipple_discharge: StrictInt = Field(
        alias="Nipple discharge", ge=0, le=1
    )

    joint_or_muscle_pain: StrictInt = Field(
        alias="Joint or muscle pain", ge=0, le=1
    )


class AssessmentRequest(BaseModel):
    """
    Complete patient assessment request.
    City is kept separate from the 35 ML features.
    """

    model_config = ConfigDict(extra="forbid")

    city: str = Field(min_length=1, max_length=100)
    patient: PatientMLInput

    @field_validator("city")
    @classmethod
    def validate_city(cls, value):
        cleaned_city = value.strip()

        if not cleaned_city:
            raise ValueError("City cannot be empty.")

        return cleaned_city

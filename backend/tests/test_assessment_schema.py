
import pytest
from pydantic import ValidationError

from app.schemas import AssessmentRequest


def test_assessment_request_rejects_empty_city():
    with pytest.raises(ValidationError):
        AssessmentRequest(city="   ", patient={})


def test_assessment_request_rejects_missing_city():
    with pytest.raises(ValidationError):
        AssessmentRequest(patient={})


def test_assessment_request_rejects_extra_fields():
    with pytest.raises(ValidationError):
        AssessmentRequest(
            city="Bengaluru",
            patient={},
            unexpected_field="invalid"
        )

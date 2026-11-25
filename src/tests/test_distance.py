
import pytest

from src.distance import calculate_distance_km


def test_same_location_returns_zero():
    distance = calculate_distance_km(
        12.9716, 77.5946,
        12.9716, 77.5946,
    )

    assert distance == 0.0


def test_distance_between_known_coordinates():
    distance = calculate_distance_km(
        0, 0,
        0, 1,
    )

    assert distance == pytest.approx(111.19, abs=0.02)


def test_distance_is_symmetric():
    distance1 = calculate_distance_km(
        12.9716, 77.5946,
        13.0358, 77.5970,
    )

    distance2 = calculate_distance_km(
        13.0358, 77.5970,
        12.9716, 77.5946,
    )

    assert distance1 == distance2


@pytest.mark.parametrize(
    "coordinates",
    [
        (91, 77.5946, 12.9716, 77.5946),
        (12.9716, 181, 12.9716, 77.5946),
        (12.9716, 77.5946, -91, 77.5946),
        (12.9716, 77.5946, 12.9716, -181),
    ],
)
def test_invalid_coordinates_raise_error(coordinates):
    with pytest.raises(ValueError):
        calculate_distance_km(*coordinates)


def test_non_finite_coordinates_raise_error():
    with pytest.raises(ValueError):
        calculate_distance_km(
            float("nan"), 77.5946,
            12.9716, 77.5946,
        )


import math


def calculate_distance_km(
    patient_latitude,
    patient_longitude,
    facility_latitude,
    facility_longitude,
):
    """
    Calculate straight-line distance between two coordinates
    using the Haversine formula.

    Returns distance in kilometres.
    """

    earth_radius_km = 6371.0

    coordinates = [
        patient_latitude,
        patient_longitude,
        facility_latitude,
        facility_longitude,
    ]

    if not all(
        isinstance(value, (int, float))
        and math.isfinite(value)
        for value in coordinates
    ):
        raise ValueError("All coordinates must be finite numbers.")

    if not -90 <= patient_latitude <= 90:
        raise ValueError("Invalid patient latitude.")

    if not -90 <= facility_latitude <= 90:
        raise ValueError("Invalid facility latitude.")

    if not -180 <= patient_longitude <= 180:
        raise ValueError("Invalid patient longitude.")

    if not -180 <= facility_longitude <= 180:
        raise ValueError("Invalid facility longitude.")

    lat1 = math.radians(patient_latitude)
    lon1 = math.radians(patient_longitude)
    lat2 = math.radians(facility_latitude)
    lon2 = math.radians(facility_longitude)

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    a = min(1.0, max(0.0, a))

    central_angle = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a),
    )

    return round(earth_radius_km * central_angle, 2)

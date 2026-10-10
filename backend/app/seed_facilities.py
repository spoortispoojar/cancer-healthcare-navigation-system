
from app.database import get_db_connection


FACILITIES = [
    {
        "facility_name": "Sample Cancer Care Centre",
        "city": "Bengaluru",
        "cancer_types": ["Breast", "Lung"],
        "services": [
            "Chemotherapy",
            "Radiation Therapy",
            "Surgery",
            "Immunotherapy",
        ],
        "address": "Sample Address, Bengaluru",
        "contact_number": None,
        "facility_type": "Cancer Care Centre",
    },
    {
        "facility_name": "Sample Oncology Hospital",
        "city": "Mysuru",
        "cancer_types": ["Breast", "Lung"],
        "services": ["Chemotherapy", "Surgery"],
        "address": "Sample Address, Mysuru",
        "contact_number": None,
        "facility_type": "Hospital",
    },
]


def seed_facilities():
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            for facility in FACILITIES:
                cursor.execute(
                    """
                    INSERT INTO facilities (
                        facility_name,
                        city,
                        cancer_types,
                        services,
                        address,
                        contact_number,
                        facility_type
                    )
                    SELECT
                        %(facility_name)s::VARCHAR(200),
                        %(city)s::VARCHAR(100),
                        %(cancer_types)s::TEXT[],
                        %(services)s::TEXT[],
                        %(address)s::TEXT,
                        %(contact_number)s::VARCHAR(20),
                        %(facility_type)s::VARCHAR(50)
                    WHERE NOT EXISTS (
                        SELECT 1
                        FROM facilities
                        WHERE facility_name = %(facility_name)s::VARCHAR(200)
                          AND city = %(city)s::VARCHAR(100)
                    );
                    """,
                    facility,
                )

        conn.commit()
        print("Sample facility records added successfully!")

    finally:
        conn.close()


if __name__ == "__main__":
    seed_facilities()

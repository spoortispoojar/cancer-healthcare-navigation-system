
from app.database import get_db_connection


def find_facilities(
    city: str,
    cancer_type: str,
    current_treatment: str,
) -> list[dict]:
    """Find facilities matching city, cancer type, and treatment."""

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    id,
                    facility_name,
                    city,
                    cancer_types,
                    services,
                    address,
                    contact_number,
                    facility_type
                FROM facilities
                WHERE LOWER(city) = LOWER(%s)
                  AND %s = ANY(cancer_types)
                  AND %s = ANY(services)
                ORDER BY facility_name;
                """,
                (
                    city.strip(),
                    cancer_type,
                    current_treatment,
                ),
            )

            rows = cursor.fetchall()
            columns = [column.name for column in cursor.description]

            return [
                dict(zip(columns, row))
                for row in rows
            ]

    finally:
        conn.close()

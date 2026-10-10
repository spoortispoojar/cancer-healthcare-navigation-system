
from app.database import get_db_connection


def create_facilities_table():
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS facilities (
                    id SERIAL PRIMARY KEY,
                    facility_name VARCHAR(200) NOT NULL,
                    city VARCHAR(100) NOT NULL,
                    cancer_types TEXT[] NOT NULL,
                    services TEXT[] NOT NULL,
                    address TEXT NOT NULL,
                    contact_number VARCHAR(20),
                    facility_type VARCHAR(50)
                );
            """)

        conn.commit()
        print("Facilities table created successfully!")

    finally:
        conn.close()


if __name__ == "__main__":
    create_facilities_table()

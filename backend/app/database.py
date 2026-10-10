
import psycopg

DATABASE_URL = "postgresql://localhost/cancer_healthcare_db"


def get_db_connection():
    """Create a connection to the project PostgreSQL database."""
    return psycopg.connect(DATABASE_URL)

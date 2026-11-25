
from sqlalchemy import text

from src.database import engine


def add_coordinate_columns():
    """Add optional latitude and longitude columns to facilities."""

    with engine.begin() as connection:
        connection.execute(
            text("""
                ALTER TABLE facilities
                ADD COLUMN IF NOT EXISTS latitude DOUBLE PRECISION
            """)
        )

        connection.execute(
            text("""
                ALTER TABLE facilities
                ADD COLUMN IF NOT EXISTS longitude DOUBLE PRECISION
            """)
        )

    print("Coordinate columns added successfully.")


if __name__ == "__main__":
    try:
        add_coordinate_columns()
    except Exception as error:
        print("Migration failed.")
        print(type(error).__name__, error)
        raise
    finally:
        engine.dispose()

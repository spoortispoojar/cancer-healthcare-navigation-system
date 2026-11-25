
import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text

from src.models import Base

from src.research_models import FacilityResearch

load_dotenv()

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("PGUSER"),
    password=os.getenv("PGPASSWORD"),
    host=os.getenv("PGHOST"),
    port=int(os.getenv("PGPORT", "5432")),
    database=os.getenv("PGDATABASE"),
)

engine = create_engine(database_url)


def create_tables():
    """Create database tables defined in models.py."""
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("Database connection successful!")

        create_tables()

        print("Tables created:")
        for table_name in Base.metadata.tables:
            print(f"- {table_name}")

    except Exception as error:
        print("Database operation failed.")
        print(type(error).__name__, error)
    finally:
        engine.dispose()

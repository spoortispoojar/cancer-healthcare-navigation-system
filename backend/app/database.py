
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Locate the backend/.env file
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"

# Load environment variables
load_dotenv(dotenv_path=ENV_FILE)

# Read the database URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not configured. "
        "Please check your backend/.env file."
    )

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Create database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for SQLAlchemy models
Base = declarative_base()


def get_db():
    """
    Provide a database session to API endpoints.
    Close the session after the request finishes.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


from sqlalchemy import text

from src.database import engine


def add_review_notes_column():
    sql = text("""
        ALTER TABLE facility_research
        ADD COLUMN IF NOT EXISTS review_notes TEXT;
    """)

    with engine.begin() as connection:
        connection.execute(sql)

    print("Review notes column is ready.")


if __name__ == "__main__":
    add_review_notes_column()

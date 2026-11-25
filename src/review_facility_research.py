
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import engine
from src.research_models import FacilityResearch


REVIEW_OPTIONS = {
    "1": (
        "REVIEWED_SUPPORTED",
        "The reviewed source explicitly supports the service claim.",
    ),
    "2": (
        "REVIEWED_NOT_SUPPORTED",
        "The reviewed source does not support the service claim.",
    ),
    "3": (
        "REVIEWED_INCONCLUSIVE",
        "The available evidence is insufficient or unclear.",
    ),
}


def save_review_notes(session, record):
    """Collect and save notes without changing the review status."""
    notes = input(
        "Describe the evidence you actually checked: "
    ).strip()

    if not notes:
        print("Notes cannot be empty. Record left unchanged.")
        return

    record.review_notes = notes

    try:
        session.flush()
        print("Note before commit:", record.review_notes)

        session.commit()
        session.refresh(record)

        print("Note after commit:", record.review_notes)

        if record.review_notes == notes:
            print("Review notes saved successfully.")
        else:
            print("WARNING: Saved note did not match the entered note.")

    except Exception as error:
        session.rollback()
        print("Could not save notes:", error)


def review_pending_records(session):
    """Review records still awaiting review."""
    records = session.scalars(
        select(FacilityResearch)
        .where(
            FacilityResearch.verification_status
            == "SOURCE_FOUND_NEEDS_REVIEW"
        )
        .order_by(FacilityResearch.research_id)
    ).all()

    if not records:
        print("No records are waiting for review.")
        return

    print(f"\nRecords awaiting review: {len(records)}")

    for record in records:
        print("\n" + "=" * 60)
        print("Research ID:", record.research_id)
        print("Facility:", record.facility_name)
        print("City:", record.city)
        print("Service:", record.service_name)
        print("Source URL:", record.source_url)

        print("\n1. Source explicitly supports this service")
        print("2. Source does not support this service")
        print("3. Evidence is unclear or insufficient")
        print("S. Skip")
        print("Q. Quit")

        choice = input("Choose an option: ").strip().upper()

        if choice == "Q":
            print("Review stopped.")
            break

        if choice == "S":
            print("Record skipped.")
            continue

        if choice not in REVIEW_OPTIONS:
            print("Invalid choice. Record left unchanged.")
            continue

        notes = input(
            "Describe the evidence you actually checked: "
        ).strip()

        if not notes:
            print("Notes are required. Record left unchanged.")
            continue

        status, assessment = REVIEW_OPTIONS[choice]

        record.verification_status = status
        record.review_notes = (
            f"{notes}\nAssessment: {assessment}"
        )
        record.reviewed_at = datetime.now(timezone.utc)
        record.is_approved = False

        try:
            session.flush()
            print("Note before commit:", record.review_notes)

            session.commit()
            session.refresh(record)

            print("Note after commit:", record.review_notes)
            print("Review status saved:", record.verification_status)
            print("Approval status:", record.is_approved)

        except Exception as error:
            session.rollback()
            print("Could not save review:", error)


def recover_missing_notes(session):
    """Add missing notes without changing existing review statuses."""
    reviewed_statuses = list(REVIEW_OPTIONS.keys())

    reviewed_status_names = [
        status for status, _ in REVIEW_OPTIONS.values()
    ]

    records = session.scalars(
        select(FacilityResearch)
        .where(
            FacilityResearch.review_notes.is_(None),
            FacilityResearch.reviewed_at.is_not(None),
            FacilityResearch.verification_status.in_(
                reviewed_status_names
            ),
        )
        .order_by(FacilityResearch.research_id)
    ).all()

    if not records:
        print("No previously reviewed records need note recovery.")
        return

    print(f"\nReviewed records missing notes: {len(records)}")
    print(
        "Enter notes based on the evidence you actually checked. "
        "This step will not change review statuses."
    )

    for record in records:
        print("\n" + "=" * 60)
        print("Research ID:", record.research_id)
        print("Facility:", record.facility_name)
        print("Service:", record.service_name)
        print("Current review status:", record.verification_status)
        print("Source URL:", record.source_url)
        print("S. Skip")
        print("Q. Quit")

        choice = input(
            "Press Enter to enter missing notes, S to skip, or Q to quit: "
        ).strip().upper()

        if choice == "Q":
            print("Recovery stopped.")
            break

        if choice == "S":
            print("Record skipped.")
            continue

        if choice:
            print("Invalid choice. Record left unchanged.")
            continue

        save_review_notes(session, record)


def main():
    with Session(engine) as session:
        while True:
            print("\n=== Facility Research Review ===")
            print("1. Review records awaiting review")
            print("2. Recover notes from already-reviewed records")
            print("3. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                review_pending_records(session)
            elif choice == "2":
                recover_missing_notes(session)
            elif choice == "3":
                print("Finished.")
                break
            else:
                print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()

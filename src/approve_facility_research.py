
"""
Explicit approval of reviewed hospital-service research records.

Only REVIEWED_SUPPORTED records are eligible.
Approval requires individual confirmation.
This module does not create facilities or service mappings.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import engine
from src.research_models import FacilityResearch


def approve_research_records():
    with Session(engine) as session:
        records = session.scalars(
            select(FacilityResearch)
            .where(
                FacilityResearch.verification_status == "REVIEWED_SUPPORTED",
                FacilityResearch.is_approved.is_(False),
            )
            .order_by(FacilityResearch.research_id)
        ).all()

        if not records:
            print("No supported records are awaiting approval.")
            return

        print("\n=== Individual Research Approval ===")
        print("Eligible records:", len(records))

        for record in records:
            print("\n-----------------------------------")
            print("Research ID:", record.research_id)
            print("Hospital:", record.facility_name)
            print("City:", record.city)
            print("Address:", record.address)
            print("Service:", record.service_name)
            print("Service code:", record.service_code)
            print("Source:", record.source_url)
            print("Review notes:", record.review_notes)

            choice = input(
                "\nType APPROVE to approve this record, "
                "S to skip, or Q to quit: "
            ).strip().upper()

            if choice == "Q":
                print("Approval process stopped.")
                break

            if choice == "APPROVE":
                record.is_approved = True
                session.commit()
                print("Record approved.")

            else:
                print("Record skipped. No changes made.")

        print("\nApproval process finished.")


if __name__ == "__main__":
    try:
        approve_research_records()
    finally:
        engine.dispose()

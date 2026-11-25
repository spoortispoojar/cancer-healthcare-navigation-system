
"""
Synchronize approved facility research into production tables.

Default: DRY RUN (no database changes).
Use --apply only after reviewing the preview.
"""

import argparse

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import engine
from src.models import Facility, FacilityService, HealthcareService
from src.research_models import FacilityResearch


def normalize(value):
    """Normalize text for safe comparison."""
    return " ".join((value or "").strip().lower().split())


def get_review_date(record):
    """Convert the review timestamp to a date."""
    if record.reviewed_at is None:
        return None
    return record.reviewed_at.date()


def build_plan(session):
    """Build a synchronization plan without changing the database."""

    records = session.scalars(
        select(FacilityResearch)
        .where(
            FacilityResearch.is_approved.is_(True),
            FacilityResearch.verification_status == "REVIEWED_SUPPORTED",
        )
        .order_by(FacilityResearch.research_id)
    ).all()

    facility_cache = {}
    service_cache = {}
    mapping_cache = set()
    planned_facilities = set()

    plan = []
    issues = []

    for record in records:

        facility_key = (
            normalize(record.facility_name),
            normalize(record.city),
            normalize(record.address),
        )

        # Validate hospital details.
        if not all(facility_key):
            issues.append(
                f"Research ID {record.research_id}: "
                "hospital name, city, or address is missing."
            )
            continue

        if facility_key[0].startswith("test"):
            issues.append(
                f"Research ID {record.research_id}: "
                "test facility names are not allowed."
            )
            continue

        # Validate service code.
        service_code = (record.service_code or "").strip().upper()

        if not service_code:
            issues.append(
                f"Research ID {record.research_id}: "
                "service code is empty."
            )
            continue

        # Validate source URL.
        if not (record.source_url or "").strip():
            issues.append(
                f"Research ID {record.research_id}: "
                "source URL is missing."
            )
            continue

        # Find exactly one production service category.
        if service_code not in service_cache:
            services = session.scalars(
                select(HealthcareService).where(
                    HealthcareService.service_code == service_code
                )
            ).all()

            if len(services) != 1:
                issues.append(
                    f"Research ID {record.research_id}: "
                    f"expected one service for {service_code}, "
                    f"found {len(services)}."
                )
                continue

            service_cache[service_code] = services[0]

        service = service_cache[service_code]

        # Find an existing hospital, or mark it for creation.
        if facility_key not in facility_cache:

            candidates = session.scalars(
                select(Facility).where(
                    Facility.city.ilike(record.city.strip()),
                    Facility.name.ilike(record.facility_name.strip()),
                )
            ).all()

            exact = [
                facility
                for facility in candidates
                if normalize(facility.address) == facility_key[2]
                and not normalize(facility.name).startswith("test")
            ]

            if len(exact) > 1:
                issues.append(
                    f"Research ID {record.research_id}: "
                    "multiple matching facilities found."
                )
                continue

            if candidates and not exact:
                issues.append(
                    f"Research ID {record.research_id}: "
                    "facility name/city exists but address differs. "
                    "Manual review required."
                )
                continue

            facility_cache[facility_key] = (
                exact[0] if exact else None
            )

        facility = facility_cache[facility_key]

        # Prevent duplicate hospital-service entries in this plan.
        mapping_key = (facility_key, service.service_id)

        if mapping_key in mapping_cache:
            plan.append({
                "record": record,
                "facility_key": facility_key,
                "service": service,
                "action": "SKIP - duplicate research entry",
            })
            continue

        mapping_cache.add(mapping_key)

        # Decide what action is required.
        if facility is None:

            if facility_key not in planned_facilities:
                action = "CREATE FACILITY AND SERVICE MAPPING"
                planned_facilities.add(facility_key)
            else:
                action = (
                    "CREATE ADDITIONAL SERVICE MAPPING "
                    "(SAME FACILITY)"
                )

        else:
            existing = session.scalar(
                select(FacilityService).where(
                    FacilityService.facility_id == facility.facility_id,
                    FacilityService.service_id == service.service_id,
                )
            )

            if existing is not None:
                action = "SKIP - mapping already exists"
            else:
                action = "CREATE SERVICE MAPPING"

        plan.append({
            "record": record,
            "facility_key": facility_key,
            "service": service,
            "action": action,
        })

    return plan, facility_cache, issues


def print_plan(plan, issues, mode):
    """Display the preview and summary."""

    print("\nAPPROVED RESEARCH SYNCHRONIZATION")
    print("================================")
    print("Mode:", mode)
    print("Eligible research entries:", len(plan))

    facility_count = sum(
        1 for item in plan
        if item["action"] == "CREATE FACILITY AND SERVICE MAPPING"
    )

    mapping_count = sum(
        1 for item in plan
        if item["action"].startswith("CREATE")
    )

    print("New facilities planned:", facility_count)
    print("New service mappings planned:", mapping_count)

    for item in plan:
        record = item["record"]

        print(f"\nResearch ID: {record.research_id}")
        print("Hospital:", record.facility_name)
        print("City:", record.city)
        print("Address:", record.address)
        print("Service:", item["service"].service_name)
        print("Service code:", item["service"].service_code)
        print("Source:", record.source_url)
        print("Action:", item["action"])

    if issues:
        print("\nITEMS REQUIRING MANUAL REVIEW")
        for issue in issues:
            print("-", issue)


def apply_plan(session, plan, facility_cache):
    """Apply the plan inside the caller's transaction."""

    for item in plan:

        if not item["action"].startswith("CREATE"):
            continue

        record = item["record"]
        key = item["facility_key"]
        service = item["service"]

        facility = facility_cache[key]

        # Create the hospital only once.
        if facility is None:
            facility = Facility(
                name=record.facility_name,
                city=record.city,
                address=record.address,
                last_verified=get_review_date(record),
            )

            session.add(facility)
            session.flush()

            # Reuse this facility for its remaining services.
            facility_cache[key] = facility

        # Check again before inserting the mapping.
        existing = session.scalar(
            select(FacilityService).where(
                FacilityService.facility_id == facility.facility_id,
                FacilityService.service_id == service.service_id,
            )
        )

        if existing is not None:
            continue

        session.add(
            FacilityService(
                facility_id=facility.facility_id,
                service_id=service.service_id,
                is_verified=True,
                verification_source=record.source_url,
                last_verified=get_review_date(record),
            )
        )


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply changes after reviewing the dry-run preview.",
    )

    args = parser.parse_args()

    # First build a preview without making changes.
    with Session(engine) as session:
        plan, facility_cache, issues = build_plan(session)

    mode = "APPLY" if args.apply else "DRY RUN"
    print_plan(plan, issues, mode)

    if not args.apply:
        print("\nDRY RUN COMPLETE. No database changes were made.")
        print("Review all entries before considering --apply.")
        return

    if issues:
        print("\nAPPLY CANCELLED: resolve all issues first.")
        return

    # Recheck and apply in one transaction.
    try:
        with Session(engine) as session:
            with session.begin():

                current_plan, current_cache, current_issues = (
                    build_plan(session)
                )

                if current_issues:
                    raise RuntimeError(
                        "Validation issues appeared during recheck."
                    )

                apply_plan(
                    session,
                    current_plan,
                    current_cache,
                )

        print("\nSynchronization completed successfully.")

    except Exception:
        print("\nSynchronization failed. Transaction rolled back.")
        raise


if __name__ == "__main__":
    main()

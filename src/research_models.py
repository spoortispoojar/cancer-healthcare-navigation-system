
from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class FacilityResearch(Base):
    __tablename__ = "facility_research"

    research_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    facility_name: Mapped[str] = mapped_column(
        String(200), nullable=False
    )

    city: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    address: Mapped[str] = mapped_column(
        String(300), nullable=False
    )

    service_name: Mapped[str] = mapped_column(
        String(200), nullable=False
    )

    service_code: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    source_url: Mapped[str] = mapped_column(
        Text, nullable=False
    )

    verification_status: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
        default="SOURCE_FOUND_NEEDS_REVIEW",
    )

    is_approved: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    reviewed_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    review_notes: Mapped[str | None] = mapped_column(
    Text, nullable=True
)


from datetime import date

from sqlalchemy import (
    Boolean,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Facility(Base):
    __tablename__ = "facilities"

    facility_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    address: Mapped[str | None] = mapped_column(String(300))
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    facility_type: Mapped[str | None] = mapped_column(String(100))
    verification_source: Mapped[str | None] = mapped_column(Text)
    last_verified: Mapped[date | None] = mapped_column(Date)

    services: Mapped[list["FacilityService"]] = relationship(
        back_populates="facility"
    )


class HealthcareService(Base):
    __tablename__ = "healthcare_services"

    service_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    service_code: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    service_name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)

    facilities: Mapped[list["FacilityService"]] = relationship(
        back_populates="service"
    )


class FacilityService(Base):
    __tablename__ = "facility_services"

    facility_service_id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    facility_id: Mapped[int] = mapped_column(
        ForeignKey("facilities.facility_id"), nullable=False
    )
    service_id: Mapped[int] = mapped_column(
        ForeignKey("healthcare_services.service_id"), nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    verification_source: Mapped[str | None] = mapped_column(Text)
    last_verified: Mapped[date | None] = mapped_column(Date)

    facility: Mapped["Facility"] = relationship(back_populates="services")
    service: Mapped["HealthcareService"] = relationship(
        back_populates="facilities"
    )

    __table_args__ = (
        UniqueConstraint(
            "facility_id", "service_id",
            name="uq_facility_service"
        ),
    )


class RecommendationRule(Base):
    __tablename__ = "recommendation_rules"

    rule_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cancer_type: Mapped[str] = mapped_column(String(30), nullable=False)
    treatment_type: Mapped[str | None] = mapped_column(String(50))
    support_level: Mapped[str | None] = mapped_column(String(20))
    symptom_key: Mapped[str | None] = mapped_column(String(100))
    required_service_id: Mapped[int] = mapped_column(
        ForeignKey("healthcare_services.service_id"), nullable=False
    )
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    required_service: Mapped["HealthcareService"] = relationship()

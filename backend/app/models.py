
from sqlalchemy import Column, Integer, String, Text, text
from sqlalchemy.dialects.postgresql import ARRAY

from app.database import Base


class Facility(Base):
    __tablename__ = "facilities"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    facility_name = Column(
        String(200),
        nullable=False
    )

    city = Column(
        String(100),
        nullable=False
    )

    cancer_types = Column(
        ARRAY(Text),
        nullable=False
    )

    services = Column(
        ARRAY(Text),
        nullable=False
    )

    address = Column(
        Text,
        nullable=False
    )

    contact_number = Column(
        String(20),
        nullable=True
    )

    facility_type = Column(
        String(50),
        nullable=True
    )

    support_services = Column(
        ARRAY(Text),
        nullable=False,
        server_default=text("'{}'::text[]")
    )

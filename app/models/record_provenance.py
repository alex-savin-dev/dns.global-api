"""RecordProvenance model — tracks which DNS records DNS.GLOBAL deployed."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class RecordProvenance(Base):
    __tablename__ = "record_provenance"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    connection_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("domain_connections.id"), nullable=False, index=True
    )
    operation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("operations.id"), nullable=False
    )
    record_type: Mapped[str] = mapped_column(Text, nullable=False)
    record_host: Mapped[str] = mapped_column(Text, nullable=False)
    record_value: Mapped[str] = mapped_column(Text, nullable=False)
    provider_record_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    connection = relationship("DomainConnection", back_populates="record_provenance")
    operation = relationship("Operation", back_populates="record_provenance")

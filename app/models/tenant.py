"""Tenant model — SaaS apps using DNS.GLOBAL."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(Text, nullable=False)
    public_key: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    secret_key_hash: Mapped[str] = mapped_column(Text, nullable=False)
    webhook_urls: Mapped[dict] = mapped_column(JSONB, server_default="'[]'::jsonb")
    webhook_secret: Mapped[str] = mapped_column(Text, nullable=False)
    template: Mapped[dict] = mapped_column(JSONB, nullable=False)
    widget_config: Mapped[dict] = mapped_column(JSONB, server_default="'{}'::jsonb")
    plan: Mapped[str] = mapped_column(Text, server_default="free")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    domain_connections = relationship("DomainConnection", back_populates="tenant")
    operations = relationship("Operation", back_populates="tenant")
    webhook_deliveries = relationship("WebhookDelivery", back_populates="tenant")
    sessions = relationship("Session", back_populates="tenant")

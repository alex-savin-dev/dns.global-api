"""Initial schema — all 7 core tables from spec section 8.1.

Revision ID: 001
Revises: None
Create Date: 2026-04-06
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # gen_random_uuid() is built-in since PG 13, no extension needed.

    # --- tenants ---
    op.create_table(
        "tenants",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("public_key", sa.Text(), nullable=False),
        sa.Column("secret_key_hash", sa.Text(), nullable=False),
        sa.Column("webhook_urls", JSONB(), server_default=sa.text("'[]'::jsonb")),
        sa.Column("webhook_secret", sa.Text(), nullable=False),
        sa.Column("template", JSONB(), nullable=False),
        sa.Column("widget_config", JSONB(), server_default=sa.text("'{}'::jsonb")),
        sa.Column("plan", sa.Text(), server_default="free"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("public_key"),
    )

    # --- domain_connections ---
    op.create_table(
        "domain_connections",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("domain", sa.Text(), nullable=False),
        sa.Column("zone", sa.Text(), nullable=True),
        sa.Column("provider", sa.Text(), nullable=True),
        sa.Column("status", sa.Text(), server_default="pending"),
        sa.Column("setup_type", sa.Text(), nullable=True),
        sa.Column("user_id", sa.Text(), nullable=True),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("tenant_id", "domain"),
    )
    op.create_index("ix_domain_connections_tenant_id", "domain_connections", ["tenant_id"])
    op.create_index("ix_domain_connections_domain", "domain_connections", ["domain"])

    # --- operations ---
    op.create_table(
        "operations",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("connection_id", UUID(as_uuid=True), sa.ForeignKey("domain_connections.id"), nullable=True),
        sa.Column("tenant_id", UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("idempotency_key", sa.Text(), nullable=True),
        sa.Column("status", sa.Text(), server_default="pending"),
        sa.Column("change_plan", JSONB(), nullable=True),
        sa.Column("result", JSONB(), nullable=True),
        sa.Column("error", JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("tenant_id", "idempotency_key"),
    )
    op.create_index("ix_operations_tenant_id", "operations", ["tenant_id"])
    op.create_index("ix_operations_connection_id", "operations", ["connection_id"])
    op.create_index("ix_operations_status", "operations", ["status"])

    # --- record_provenance ---
    op.create_table(
        "record_provenance",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("connection_id", UUID(as_uuid=True), sa.ForeignKey("domain_connections.id"), nullable=False),
        sa.Column("operation_id", UUID(as_uuid=True), sa.ForeignKey("operations.id"), nullable=False),
        sa.Column("record_type", sa.Text(), nullable=False),
        sa.Column("record_host", sa.Text(), nullable=False),
        sa.Column("record_value", sa.Text(), nullable=False),
        sa.Column("provider_record_id", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_record_provenance_connection_id", "record_provenance", ["connection_id"])

    # --- operation_log ---
    op.create_table(
        "operation_log",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("operation_id", UUID(as_uuid=True), sa.ForeignKey("operations.id"), nullable=False),
        sa.Column("state_from", sa.Text(), nullable=True),
        sa.Column("state_to", sa.Text(), nullable=True),
        sa.Column("detail", JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_operation_log_operation_id", "operation_log", ["operation_id"])

    # --- webhook_deliveries ---
    op.create_table(
        "webhook_deliveries",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("tenant_id", UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("operation_id", UUID(as_uuid=True), sa.ForeignKey("operations.id"), nullable=False),
        sa.Column("event", sa.Text(), nullable=False),
        sa.Column("payload", JSONB(), nullable=False),
        sa.Column("status", sa.Text(), server_default="pending"),
        sa.Column("attempts", sa.Integer(), server_default="0"),
        sa.Column("last_attempt_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("next_retry_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("response_code", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_webhook_deliveries_tenant_id", "webhook_deliveries", ["tenant_id"])
    op.create_index("ix_webhook_deliveries_status", "webhook_deliveries", ["status"])

    # --- sessions ---
    op.create_table(
        "sessions",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("token_hash", sa.Text(), nullable=False),
        sa.Column("tenant_id", UUID(as_uuid=True), sa.ForeignKey("tenants.id"), nullable=False),
        sa.Column("user_id", sa.Text(), nullable=True),
        sa.Column("domain", sa.Text(), nullable=True),
        sa.Column("nonce", sa.Text(), nullable=False),
        sa.Column("used", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("token_hash"),
    )
    op.create_index("ix_sessions_tenant_id", "sessions", ["tenant_id"])
    op.create_index("ix_sessions_expires_at", "sessions", ["expires_at"])


def downgrade() -> None:
    op.drop_table("sessions")
    op.drop_table("webhook_deliveries")
    op.drop_table("operation_log")
    op.drop_table("record_provenance")
    op.drop_table("operations")
    op.drop_table("domain_connections")
    op.drop_table("tenants")

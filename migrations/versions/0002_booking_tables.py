"""booking tables

Revision ID: 0002_booking_tables
Revises: 0001_init_users
Create Date: 2026-07-04
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0002_booking_tables"
down_revision = "0001_init_users"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "booking_resources",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "booking_bookings",
        sa.Column("id", sa.dialects.postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column(
            "resource_id",
            sa.dialects.postgresql.UUID(as_uuid=True),
            sa.ForeignKey("booking_resources.id"),
            nullable=False,
        ),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="confirmed"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_booking_bookings_resource_id", "booking_bookings", ["resource_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_booking_bookings_resource_id", table_name="booking_bookings")
    op.drop_table("booking_bookings")
    op.drop_table("booking_resources")


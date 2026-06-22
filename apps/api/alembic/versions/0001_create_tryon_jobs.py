"""create tryon_jobs

Revision ID: 0001
Revises:
Create Date: 2026-06-22

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tryon_jobs",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("mode", sa.String(length=32), nullable=False),
        sa.Column("request", sa.JSON(), nullable=False),
        sa.Column("result", sa.JSON(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_tryon_jobs_user_id", "tryon_jobs", ["user_id"])
    op.create_index("ix_tryon_jobs_status", "tryon_jobs", ["status"])


def downgrade() -> None:
    op.drop_index("ix_tryon_jobs_status", table_name="tryon_jobs")
    op.drop_index("ix_tryon_jobs_user_id", table_name="tryon_jobs")
    op.drop_table("tryon_jobs")

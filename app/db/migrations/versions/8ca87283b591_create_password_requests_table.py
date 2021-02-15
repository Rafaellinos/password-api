"""create password_requests table

Revision ID: 8ca87283b591
Revises: 36be2dec810f
Create Date: 2021-02-14 18:43:22.546531

"""
import pathlib
import sys
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = '8ca87283b591'
down_revision = '36be2dec810f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "password_requests",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("create_date", sa.DateTime),
        sa.Column("public_id", UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("due_date", sa.DateTime),
        sa.Column("view_counter", sa.Integer),
        sa.Column("status", sa.Enum('valid', 'expired', name="status")),
    )


def downgrade():
    op.drop_table("password_requests")

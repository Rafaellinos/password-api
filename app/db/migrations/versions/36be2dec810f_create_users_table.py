"""create users table

Revision ID: 36be2dec810f
Revises: 
Create Date: 2021-02-14 18:09:40.958036

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '36be2dec810f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("public_id", UUID(as_uuid=True), nullable=False),
        sa.Column("username", sa.String, nullable=False),
        sa.Column("is_active", sa.Boolean),
        sa.Column("password", sa.String),
    )


def downgrade():
    op.drop_table("users")

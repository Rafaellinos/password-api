"""create password table

Revision ID: 870b32a665dd
Revises: 8ca87283b591
Create Date: 2021-02-14 18:58:37.880285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '870b32a665dd'
down_revision = '8ca87283b591'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "password",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("password", sa.String),
        sa.Column("password_requests_id", sa.Integer, sa.ForeignKey("password_requests.id")),
    )


def downgrade():
    pass

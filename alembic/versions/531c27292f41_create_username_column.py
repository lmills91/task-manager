"""create user table

Revision ID: 531c27292f41
Revises: 
Create Date: 2023-11-28 20:48:46.978210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "531c27292f41"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("username", sa.String(200), unique=True, index=True)
    )


def downgrade() -> None:
    op.drop_column("users", "username")

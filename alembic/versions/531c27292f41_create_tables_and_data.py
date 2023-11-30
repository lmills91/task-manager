"""create user table

Revision ID: 531c27292f41
Revises: 
Create Date: 2023-11-28 20:48:46.978210

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "531c27292f41"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    users = op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True, autoincrement=True),
        sa.Column("email", sa.String(50), unique=True, index=True),
        sa.Column("username", sa.String(200), unique=True, index=True),
    )

    tasks = op.create_table(
        "tasks",
        sa.Column("id", sa.Integer, primary_key=True, index=True, autoincrement=True),
        sa.Column("title", sa.String(80), index=True),
        sa.Column("description", sa.String(200), index=True),
        sa.Column("status", sa.String(15), index=True, default="Pending"),
        sa.Column("deleted", sa.Boolean, default=False),
        sa.Column("due_date", sa.DateTime, default=None),
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id")),
    )

    history = op.create_table(
        "history",
        sa.Column("id", sa.Integer, primary_key=True, index=True, autoincrement=True),
        sa.Column("date_created", sa.DateTime, default=datetime.datetime.utcnow()),
        sa.Column("action", sa.String(20), nullable=False),
        sa.Column("owner_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("task_id", sa.Integer, sa.ForeignKey("tasks.id")),
    )

    op.bulk_insert(
        users,
        [
            {"email": "test1@test.com", "username": "test1"},
            {"email": "test2@test.com", "username": "test2"},
            {"email": "test3@test.com", "username": "test3"},
        ],
    )

    op.bulk_insert(
        tasks,
        [
            {
                "title": "task 1",
                "description": "description of task 1",
                "status": "Pending",
                "deleted": False,
                "due_date": None,
                "owner_id": 1,
            },
            {
                "title": "task 2",
                "description": "description of task 2",
                "status": "Pending",
                "deleted": False,
                "due_date": None,
                "owner_id": 2,
            },
            {
                "title": "task 3",
                "description": "description of task 3",
                "status": "Pending",
                "deleted": False,
                "due_date": None,
                "owner_id": 1,
            },
            {
                "title": "task 4",
                "description": "description of task 4",
                "status": "Pending",
                "deleted": False,
                "due_date": None,
                "owner_id": 2,
            },
            {
                "title": "task 5",
                "description": "description of task 5",
                "status": "Pending",
                "deleted": False,
                "due_date": None,
                "owner_id": 1,
            },
            {
                "title": "task 6",
                "description": "description of task 6",
                "status": "Pending",
                "deleted": False,
                "due_date": None,
                "owner_id": 3,
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("history")
    op.drop_table("tasks")
    op.drop_table("users")

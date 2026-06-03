"""create customers

Revision ID: 8bc5cc191cdc
Revises: 
Create Date: 2026-05-20 17:20:53.071459

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bc5cc191cdc'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute(
        """
        CREATE TABLE customers(
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL
        );
        """
    )


def downgrade():
    op.execute (
        """ DROP TABLE customers;
        """
    )

"""create user

Revision ID: 1119930645a1
Revises: 
Create Date: 2024-12-13 14:11:26.334164

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1119930645a1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('email', sa.String(100), unique=True),
        sa.Column('first_name', sa.String(100)),
        sa.Column('last_name', sa.String(100)),
        sa.Column('hashed_password', sa.String(100)),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('role', sa.String(100))
    )


def downgrade() -> None:
    op.drop_table('users')

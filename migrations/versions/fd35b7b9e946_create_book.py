"""create book

Revision ID: fd35b7b9e946
Revises: 1119930645a1
Create Date: 2024-12-13 14:13:30.618713

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd35b7b9e946'
down_revision: Union[str, None] = '1119930645a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'books',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('title', sa.String(100)),
        sa.Column('author', sa.String(100)),
        sa.Column('owner_id', sa.Integer,
                  sa.ForeignKey('users.id'))
    )


def downgrade() -> None:
    op.drop_table('books')

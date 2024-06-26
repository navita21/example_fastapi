"""addlast few columns to posts table

Revision ID: 2cc2701fec63
Revises: 9218ed8fc96d
Create Date: 2024-06-26 14:19:37.070285

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cc2701fec63'
down_revision: Union[str, None] = '9218ed8fc96d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('city',sa.String(), nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),nullable=False, server_default=
                                     sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('posts','city')
    op.drop_column('posts','created_at')
    pass

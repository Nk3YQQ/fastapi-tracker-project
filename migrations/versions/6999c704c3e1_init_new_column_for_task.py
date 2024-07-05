"""Init new column for Task

Revision ID: 6999c704c3e1
Revises: e92a1e0dcdc7
Create Date: 2024-07-05 11:35:08.443454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6999c704c3e1'
down_revision: Union[str, None] = 'e92a1e0dcdc7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('deadline', sa.Date(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'deadline')
    # ### end Alembic commands ###

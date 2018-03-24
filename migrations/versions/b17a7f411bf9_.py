"""empty message

Revision ID: b17a7f411bf9
Revises: eabff477b1da
Create Date: 2018-03-25 00:44:34.381104

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b17a7f411bf9'
down_revision = 'eabff477b1da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('token', sa.Column('blacklisted_at', sa.DateTime(), nullable=True))
    op.drop_column('token', 'blacklist_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('token', sa.Column('blacklist_time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('token', 'blacklisted_at')
    # ### end Alembic commands ###
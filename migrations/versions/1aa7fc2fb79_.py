"""empty message

Revision ID: 1aa7fc2fb79
Revises: 419aae7e9c5
Create Date: 2015-01-14 23:07:15.712183

"""

# revision identifiers, used by Alembic.
revision = '1aa7fc2fb79'
down_revision = '419aae7e9c5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group_membership', sa.Column('last_updated', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('group_membership', 'last_updated')
    ### end Alembic commands ###

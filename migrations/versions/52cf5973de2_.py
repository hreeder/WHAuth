"""empty message

Revision ID: 52cf5973de2
Revises: 2ecc9f25f6
Create Date: 2015-01-06 11:14:08.980499

"""

# revision identifiers, used by Alembic.
revision = '52cf5973de2'
down_revision = '2ecc9f25f6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('superuser', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'superuser')
    ### end Alembic commands ###

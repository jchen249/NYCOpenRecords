"""Added point of contact

Revision ID: c7f05adcf7d9
Revises: 13de5f42768b
Create Date: 2018-03-28 19:04:41.813259

"""

# revision identifiers, used by Alembic.
revision = 'c7f05adcf7d9'
down_revision = '7ba6fbb131bb'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_requests', sa.Column('point_of_contact', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_requests', 'point_of_contact')
    ### end Alembic commands ###

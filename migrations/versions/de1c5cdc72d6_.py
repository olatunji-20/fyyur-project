"""empty message

Revision ID: de1c5cdc72d6
Revises: a45e4068a731
Create Date: 2022-08-12 04:07:56.927350

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de1c5cdc72d6'
down_revision = 'a45e4068a731'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('description', sa.String(), nullable=True))
    op.add_column('artist', sa.Column('website_link', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artist', 'website_link')
    op.drop_column('artist', 'description')
    # ### end Alembic commands ###
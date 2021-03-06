"""add language to predictions

Revision ID: 0ffc605bd791
Revises: b6a325a8cb14
Create Date: 2020-01-30 19:18:20.231956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ffc605bd791'
down_revision = 'b6a325a8cb14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('prediction', sa.Column('language', sa.String(length=5), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('prediction', 'language')
    # ### end Alembic commands ###

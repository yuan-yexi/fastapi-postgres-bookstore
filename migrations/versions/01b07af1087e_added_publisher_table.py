"""Added publisher table

Revision ID: 01b07af1087e
Revises: 8802674aa8f5
Create Date: 2023-04-14 10:31:29.939268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01b07af1087e'
down_revision = '8802674aa8f5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('publisher',
    sa.Column('_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('_id')
    )
    op.create_index(op.f('ix_publisher__id'), 'publisher', ['_id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_publisher__id'), table_name='publisher')
    op.drop_table('publisher')
    # ### end Alembic commands ###
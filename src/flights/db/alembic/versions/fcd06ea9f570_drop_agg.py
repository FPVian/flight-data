"""drop_agg

Revision ID: fcd06ea9f570
Revises: 92f5f2e783a8
Create Date: 2023-10-27 18:22:31.821573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcd06ea9f570'
down_revision = '92f5f2e783a8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('flight_aggregates')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('flight_aggregates',
    sa.Column('sample_entry_date_utc', sa.DATETIME(), nullable=False),
    sa.Column('number_of_flights', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('sample_entry_date_utc')
    )
    # ### end Alembic commands ###

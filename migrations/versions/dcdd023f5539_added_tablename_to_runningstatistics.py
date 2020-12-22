"""added tablename to runningstatistics

Revision ID: dcdd023f5539
Revises: e52eca539eae
Create Date: 2020-12-18 15:00:29.068930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcdd023f5539'
down_revision = 'e52eca539eae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('runningstatistics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mile_pr', sa.String(length=10), nullable=True),
    sa.Column('fivek_pr', sa.String(length=10), nullable=True),
    sa.Column('tenk_pr', sa.String(length=10), nullable=True),
    sa.Column('half_pr', sa.String(length=10), nullable=True),
    sa.Column('marathon_pr', sa.String(length=10), nullable=True),
    sa.Column('fiftyk_pr', sa.String(length=10), nullable=True),
    sa.Column('hundrek_pr', sa.String(length=10), nullable=True),
    sa.Column('fiftym_pr', sa.String(length=10), nullable=True),
    sa.Column('hundredm_pr', sa.String(length=10), nullable=True),
    sa.Column('running_streak_pr', sa.Integer(), nullable=True),
    sa.Column('annual_miles_pr', sa.Integer(), nullable=True),
    sa.Column('most_races_year', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('running_statistics')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('running_statistics',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('mile_pr', sa.VARCHAR(length=10), nullable=True),
    sa.Column('fivek_pr', sa.VARCHAR(length=10), nullable=True),
    sa.Column('tenk_pr', sa.VARCHAR(length=10), nullable=True),
    sa.Column('half_pr', sa.VARCHAR(length=10), nullable=True),
    sa.Column('marathon_pr', sa.VARCHAR(length=10), nullable=True),
    sa.Column('fiftyk_pr', sa.VARCHAR(length=10), nullable=True),
    sa.Column('hundrek_pr', sa.VARCHAR(length=10), nullable=True),
    sa.Column('fiftym_pr', sa.VARCHAR(length=10), nullable=True),
    sa.Column('hundredm_pr', sa.VARCHAR(length=10), nullable=True),
    sa.Column('running_streak_pr', sa.INTEGER(), nullable=True),
    sa.Column('annual_miles_pr', sa.INTEGER(), nullable=True),
    sa.Column('most_races_year', sa.INTEGER(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.drop_table('runningstatistics')
    # ### end Alembic commands ###
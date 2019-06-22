"""initial

Revision ID: f6778600730b
Revises: 
Create Date: 2019-06-22 15:15:28.299286

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f6778600730b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('files',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('name', postgresql.UUID(), nullable=True),
    sa.Column('data', postgresql.BYTEA(), nullable=True),
    sa.Column('passport_data', postgresql.BYTEA(), nullable=True),
    sa.Column('user_id', postgresql.UUID(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('incedents',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), nullable=True),
    sa.Column('created_by', postgresql.UUID(), nullable=True),
    sa.Column('logituide', sa.INTEGER(), nullable=True),
    sa.Column('latitude', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('incedents_points',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('email', sa.VARCHAR(), nullable=True),
    sa.Column('phone', sa.VARCHAR(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('comfirmed', sa.BOOLEAN(), nullable=True),
    sa.Column('comfirm_code', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('vehicle',
    sa.Column('plate', sa.VARCHAR(), nullable=False),
    sa.Column('owner_id', postgresql.UUID(), nullable=True),
    sa.Column('car_id', postgresql.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('plate', 'car_id'),
    sa.UniqueConstraint('plate')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vehicle')
    op.drop_table('users')
    op.drop_table('incedents_points')
    op.drop_table('incedents')
    op.drop_table('files')
    # ### end Alembic commands ###
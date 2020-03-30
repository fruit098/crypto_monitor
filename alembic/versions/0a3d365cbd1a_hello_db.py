"""Hello DB

Revision ID: 0a3d365cbd1a
Revises: 
Create Date: 2020-03-30 17:56:48.676590

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0a3d365cbd1a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('node',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('user_agent', sa.String(), nullable=True),
    sa.Column('highest_protocol', sa.String(), nullable=True),
    sa.Column('services', postgresql.ARRAY(sa.String()), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ip_pool',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('ip', sa.String(), nullable=True),
    sa.Column('last_seen', sa.DateTime(timezone=True), nullable=True),
    sa.Column('inserted', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('node_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['node_id'], ['node.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ip_pool_ip'), 'ip_pool', ['ip'], unique=True)
    op.create_table('node_activity',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('start_of_activity', sa.DateTime(timezone=True), nullable=True),
    sa.Column('end_of_activity', sa.DateTime(timezone=True), nullable=True),
    sa.Column('node_id', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['node_id'], ['node.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('node_activity')
    op.drop_index(op.f('ix_ip_pool_ip'), table_name='ip_pool')
    op.drop_table('ip_pool')
    op.drop_table('node')
    # ### end Alembic commands ###
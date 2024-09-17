"""empty message

Revision ID: 8b7b6ce91a14
Revises: b00ba0c69a2d
Create Date: 2024-09-17 11:41:20.317738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b7b6ce91a14'
down_revision = 'b00ba0c69a2d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('starship',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('model', sa.Float(), nullable=False),
    sa.Column('manufacturer', sa.Float(), nullable=False),
    sa.Column('cost_in_credits', sa.String(length=250), nullable=False),
    sa.Column('length', sa.String(length=250), nullable=False),
    sa.Column('crew', sa.String(length=250), nullable=False),
    sa.Column('passengers', sa.String(length=250), nullable=False),
    sa.Column('cargo_capacity', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('starship_fav',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('starship_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['starship_id'], ['starship.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('starship_fav')
    op.drop_table('starship')
    # ### end Alembic commands ###

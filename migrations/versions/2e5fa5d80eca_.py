"""empty message

Revision ID: 2e5fa5d80eca
Revises: a5cffa318ac2
Create Date: 2024-05-18 19:16:42.016193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e5fa5d80eca'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.Column('birth_year', sa.String(length=250), nullable=True),
    sa.Column('eye_color', sa.String(length=250), nullable=True),
    sa.Column('gender', sa.String(length=250), nullable=True),
    sa.Column('hair_color', sa.String(length=250), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('homeworld', sa.String(length=250), nullable=True),
    sa.Column('mass', sa.Integer(), nullable=True),
    sa.Column('skin_color', sa.String(length=250), nullable=True),
    sa.Column('created', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('edited', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('url', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('climate', sa.String(length=250), nullable=True),
    sa.Column('diameter', sa.Numeric(), nullable=True),
    sa.Column('gravity', sa.Numeric(), nullable=True),
    sa.Column('created', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('edited', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.Column('orbital_period', sa.Integer(), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('rotation_period', sa.Integer(), nullable=True),
    sa.Column('surface_water', sa.Integer(), nullable=True),
    sa.Column('terrain', sa.String(length=250), nullable=True),
    sa.Column('url', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite_person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('person_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['person_id'], ['person.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorite_planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('planet_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['planet_id'], ['planet.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorite_planet')
    op.drop_table('favorite_person')
    op.drop_table('planet')
    op.drop_table('person')
    # ### end Alembic commands ###

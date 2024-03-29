"""empty message

Revision ID: 6c62648c6a16
Revises: 4ca96a98ceb4
Create Date: 2019-07-02 01:53:32.916451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c62648c6a16'
down_revision = '4ca96a98ceb4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('produtos', sa.Column('prod_arquivo', sa.String(length=64), nullable=True))
    op.create_unique_constraint(None, 'produtos', ['prod_arquivo'])
    op.create_unique_constraint(None, 'produtos', ['prod_nome'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'produtos', type_='unique')
    op.drop_constraint(None, 'produtos', type_='unique')
    op.drop_column('produtos', 'prod_arquivo')
    # ### end Alembic commands ###

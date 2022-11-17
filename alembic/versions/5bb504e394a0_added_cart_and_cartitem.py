"""Added cart and cartitem

Revision ID: 5bb504e394a0
Revises: 24e4d867bd80
Create Date: 2022-11-17 10:38:56.868288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bb504e394a0'
down_revision = '24e4d867bd80'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cart',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('total_quantity', sa.Integer(), nullable=True),
    sa.Column('total_price', sa.Integer(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cart_id'), 'cart', ['id'], unique=False)
    op.create_table('cartitem',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('book_id', sa.BigInteger(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('cart_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['cart_id'], ['cart.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cartitem_id'), 'cartitem', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_cartitem_id'), table_name='cartitem')
    op.drop_table('cartitem')
    op.drop_index(op.f('ix_cart_id'), table_name='cart')
    op.drop_table('cart')
    # ### end Alembic commands ###

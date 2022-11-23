"""Altered cart status choice field

Revision ID: 750857a1ea02
Revises: c75b644d6516
Create Date: 2022-11-22 10:57:37.862333

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '750857a1ea02'
down_revision = 'c75b644d6516'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_orderitem_id', table_name='orderitem')
    op.drop_table('orderitem')
    op.drop_index('ix_order_id', table_name='order')
    op.drop_table('order')
    op.alter_column('cart', 'status',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cart', 'status',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.create_table('order',
    sa.Column('id', sa.BIGINT(), server_default=sa.text("nextval('order_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('total_quantity', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('total_price', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('cart_id', sa.BIGINT(), autoincrement=False, nullable=True),
    sa.Column('user_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['cart_id'], ['cart.id'], name='order_cart_id_fkey', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='order_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='order_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_order_id', 'order', ['id'], unique=False)
    op.create_table('orderitem',
    sa.Column('id', sa.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('book_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('order_id', sa.BIGINT(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], name='orderitem_book_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], name='orderitem_order_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='orderitem_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='orderitem_pkey')
    )
    op.create_index('ix_orderitem_id', 'orderitem', ['id'], unique=False)
    # ### end Alembic commands ###

"""init

Revision ID: 18ded73d8e54
Revises: 
Create Date: 2022-11-15 07:37:53.734989

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '18ded73d8e54'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('username', sa.String(250), nullable=False),
        sa.Column('password', sa.String(250)),
        sa.Column('first_name', sa.String(150)),
        sa.Column('last_name', sa.String(150)),
        sa.Column('email', sa.String(150)),
        sa.Column('phone', sa.BigInteger),
        sa.Column('location', sa.String(150)),
        sa.Column('is_superuser', sa.Boolean()),
    )


def downgrade() -> None:
    op.drop_table('user')

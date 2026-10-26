"""added other fields

Revision ID: 0efe6a221436
Revises: f7f7e024868a
Create Date: 2026-10-08 14:39:34.452663

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0efe6a221436'
down_revision = 'f7f7e024868a'
branch_labels = None
depends_on = None


def upgrade():

    # Add the new columns
    with op.batch_alter_table('admins', schema=None) as batch_op:

        batch_op.add_column(
            sa.Column(
                'phone',
                sa.String(length=20),
                nullable=True
            )
        )

        batch_op.add_column(
            sa.Column(
                'password_changed_at',
                sa.DateTime(),
                nullable=True
            )
        )

        batch_op.add_column(
            sa.Column(
                'last_login',
                sa.DateTime(),
                nullable=True
            )
        )

        # Existing admins need a value first,
        # so this is temporarily nullable.
        batch_op.add_column(
            sa.Column(
                'is_active',
                sa.Boolean(),
                nullable=True
            )
        )

        # is_super_admin is now NOT NULL
        batch_op.alter_column(
            'is_super_admin',
            existing_type=sa.BOOLEAN(),
            nullable=False
        )

        # Give the phone unique constraint an explicit name
        batch_op.create_unique_constraint(
            'uq_admins_phone',
            ['phone']
        )


def downgrade():

    with op.batch_alter_table('admins', schema=None) as batch_op:

        batch_op.drop_constraint(
            'uq_admins_phone',
            type_='unique'
        )

        batch_op.alter_column(
            'is_super_admin',
            existing_type=sa.BOOLEAN(),
            nullable=True
        )

        batch_op.drop_column('is_active')
        batch_op.drop_column('last_login')
        batch_op.drop_column('password_changed_at')
        batch_op.drop_column('phone')
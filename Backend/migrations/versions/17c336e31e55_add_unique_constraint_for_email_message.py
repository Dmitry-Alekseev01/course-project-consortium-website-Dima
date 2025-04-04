"""Add unique constraint for email+message

Revision ID: 17c336e31e55
Revises: 
Create Date: 2025-03-27 13:57:47.883838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17c336e31e55'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('contact', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_email_message', ['email', 'message'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('contact', schema=None) as batch_op:
        batch_op.drop_constraint('uq_email_message', type_='unique')

    # ### end Alembic commands ###

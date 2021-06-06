"""empty message

Revision ID: ecfc6488a6c8
Revises: 96788629305d
Create Date: 2021-04-13 13:58:40.542157

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ecfc6488a6c8'
down_revision = '96788629305d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('session_v2',
                    sa.Column('id',
                              sa.Integer(),
                              autoincrement=True,
                              nullable=False,
                              comment='session id'),
                    sa.Column('jti',
                              sa.String(length=64),
                              nullable=True,
                              comment='JWT jti'),
                    sa.Column(
                        'expired_at',
                        sa.DateTime(timezone=True),
                        server_default=sa.text('now()'),
                        nullable=True,
                        comment='expired time, for db automatically clear'),
                    sa.Column('created_at',
                              sa.DateTime(timezone=True),
                              server_default=sa.text('now()'),
                              nullable=True,
                              comment='created at'),
                    sa.PrimaryKeyConstraint('id'),
                    comment='This is webconsole session table',
                    mysql_charset='utf8mb4',
                    mysql_engine='innodb')
    op.create_index('idx_jti', 'session_v2', ['jti'], unique=False)
    # Delete expired token every 30 minutes
    op.execute(
        'CREATE EVENT IF NOT EXISTS token_event ON SCHEDULE EVERY 30 MINUTE DO '
        'DELETE FROM session_v2 '
        'WHERE TIMESTAMPDIFF(SECOND, NOW(), `expired_at`) < 0;')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_jti', table_name='session_v2')
    op.drop_table('session_v2')
    op.execute('DROP EVENT token_event;')
    # ### end Alembic commands ###

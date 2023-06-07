"""initialize

Revision ID: 1701a835db6c
Revises: 
Create Date: 2023-05-16 22:30:02.734136

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1701a835db6c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('(now())')),
        sa.Column('username', sa.String(length=64), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password', sa.String(length=64), nullable=True),
        sa.Column('activated', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    op.create_table(
        'movies',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('(now())')),
        sa.Column('title', sa.String(length=64), nullable=False),
        sa.Column('duration', sa.Time(), nullable=False),
        sa.Column('category', sa.String(length=64), nullable=False),
        sa.Column('description', sa.String(length=2000), nullable=True),
        sa.Column('picture_url', sa.String(length=255), nullable=True)
    )
    op.create_table(
        'cinemas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('(now())')),
        sa.Column('name', sa.String(length=64), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'showtimes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('(now())')),
        sa.Column('movie_id', sa.Integer(), nullable=False),
        sa.Column('cinema_id', sa.Integer(), nullable=False),
        sa.Column('movie_start_time', sa.TIMESTAMP(
            timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['cinema_id'], ['cinemas.id'], ),
        sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'seats',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cinema_id', sa.Integer(), nullable=False),
        sa.Column('seat_number', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['cinema_id'], ['cinemas.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'reservations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.text('(now())')),
        sa.Column('showtime_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(
            ['showtime_id'], ['showtimes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'reservation_seat',
        sa.Column('reservation_id', sa.Integer(), nullable=False),
        sa.Column('seat_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['reservation_id'], [
                                'reservations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['seat_id'], ['seats.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('reservation_id', 'seat_id')
    )


def downgrade():
    op.drop_table('reservation_seat')
    op.drop_table('reservations')
    op.drop_table('seats')
    op.drop_table('showtimes')
    op.drop_table('cinemas')
    op.drop_table('movies')
    op.drop_table('users')

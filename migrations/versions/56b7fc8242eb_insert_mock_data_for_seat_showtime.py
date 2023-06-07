"""insert mock data for seat showtime

Revision ID: 56b7fc8242eb
Revises: c83be22f9b23
Create Date: 2023-05-16 22:52:34.794994

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56b7fc8242eb'
down_revision = 'c83be22f9b23'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Insert mock data into showtimes table
    op.execute(
        """
            INSERT INTO showtimes (movie_id, cinema_id, movie_start_time)
            VALUES 
            (1, 1, '2023-06-20 18:00:00'),
            (2, 2, '2023-06-20 20:30:00'),
            (1, 2, '2023-06-21 16:00:00'),
            (3, 1, '2023-06-21 18:30:00'),
            (2, 1, '2023-06-21 20:00:00'),
            (4, 2, '2023-06-22 15:30:00'),
            (5, 1, '2023-06-22 17:00:00'),
            (3, 1, '2023-06-22 19:30:00'),
            (6, 1, '2023-06-23 14:00:00'),
            (4, 2, '2023-06-23 16:30:00'),
            (2, 1, '2023-06-23 19:00:00'),
            (5, 2, '2023-06-24 12:30:00'),
            (1, 1, '2023-06-24 15:00:00'),
            (6, 2, '2023-06-24 17:30:00'),
            (3, 1, '2023-06-25 14:00:00'),
            (4, 2, '2023-06-25 16:30:00'),
            (5, 1, '2023-06-25 19:00:00'),
            (2, 2, '2023-06-26 13:30:00'),
            (6, 1, '2023-06-26 16:00:00'),
            (1, 2, '2023-06-26 18:30:00')
        """
    )

    # Insert mock data into seats table
    op.execute(
        """
        DO $$ 
        BEGIN
        FOR cinema_id IN 1..2 -- Adjust the range based on your cinema ids
        LOOP
            -- Insert seat numbers from 1 to 200
            FOR seat_number IN 1..200
            LOOP
            INSERT INTO seats (cinema_id, seat_number)
            VALUES (cinema_id, seat_number);
            END LOOP;
        END LOOP;
        END $$;
        """
    )


def downgrade() -> None:
    pass

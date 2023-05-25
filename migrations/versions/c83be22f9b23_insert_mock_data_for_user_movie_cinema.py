"""insert mock data for user movie cinema

Revision ID: c83be22f9b23
Revises: 1701a835db6c
Create Date: 2023-05-16 22:48:44.136383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c83be22f9b23'
down_revision = '1701a835db6c'
branch_labels = None
depends_on = None


def upgrade():
    # ... existing table creation code ...

    # Insert mock data into users table
    op.execute(
        """
        INSERT INTO users (username, email, password, activated)
        VALUES ('admin', 'admin@example.com', 'password', True)
        """
    )

    # Insert mock data into movies table
    op.execute(
        """
        INSERT INTO movies (title, duration, category, description, picture_url)
        VALUES ('Movie 1', '02:30:00', 'Action', 'Movie 1 description', 'https://miro.medium.com/v2/resize:fit:1260/format:webp/1*MBb7iatu9etCcQQGxUXpbg.jpeg'),
               ('Movie 2', '01:45:00', 'Drama', 'Movie 2 description', 'https://3.bp.blogspot.com/-L0I2Milxdtc/W3P87r_qCtI/AAAAAAAAH68/iY0dAZpXlbEmurbprcnTACoFIbFlfQiCQCKgBGAs/s1600/cyan_bg_.jpg')
        """
    )

    # Insert mock data into cinemas table
    op.execute(
        """
        INSERT INTO cinemas (name)
        VALUES ('Cinema A'),
               ('Cinema B')
        """
    )


def downgrade() -> None:
    pass

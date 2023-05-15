INSERT INTO users (created_at, username, email, password, activated)
VALUES
    ('2023-05-15 10:00:00+00:00', 'admin', 'admin@example.com', 'password', true)

INSERT INTO movies (created_at, title, duration, category)
VALUES
    ('2023-06-20 10:00:00+00:00', 'Avengers: Endgame', '3 hours'::interval, 'Action'),
    ('2023-06-20 11:30:00+00:00', 'The Lion King', '1 hour 58 minutes'::interval, 'Animation'),
    ('2023-06-20 12:45:00+00:00', 'Joker', '2 hours 2 minutes'::interval, 'Drama');


INSERT INTO cinemas (created_at, title)
VALUES
    ('2023-05-15 10:00:00+00:00', 'A'),
    ('2023-05-15 11:30:00+00:00', 'B'),
    ('2023-05-15 12:45:00+00:00', 'C');



INSERT INTO showtime (created_at, movie_id, cinema_id, movie_start_time)
VALUES
    ('2023-05-15 10:00:00+00:00', 1, 1, '2023-06-20 13:00:00+00:00'),
    ('2023-05-15 10:00:00+00:00', 2, 2, '2023-06-20 14:00:00+00:00'),
    ('2023-05-15 10:00:00+00:00', 3, 3, '2023-06-20 16:30:00+00:00');


DO $$ 
BEGIN
  FOR cinema_id IN 1..3 -- Adjust the range based on your cinema ids
  LOOP
    -- Insert seat numbers from 1 to 200
    FOR seat_number IN 1..200
    LOOP
      INSERT INTO seats (cinemas_id, seat_number)
      VALUES (cinema_id, seat_number);
    END LOOP;
  END LOOP;
END $$;
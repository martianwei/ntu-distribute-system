CREATE TABLE IF NOT EXISTS users (
    id serial PRIMARY KEY,
    created_at timestamp(0) with time zone NOT NULL DEFAULT NOW(),
    username varchar(64) NOT NULL,
    email varchar(255) UNIQUE NOT NULL,
    password varchar(64) DEFAULT NULL,
    activated boolean NOT NULL
);

CREATE TABLE IF NOT EXISTS movies(
    id serial PRIMARY KEY,
    created_at timestamp(0) with time zone NOT NULL DEFAULT NOW(),
    title varchar(64) NOT NULL,
    duration TIME,
    category varchar(64) NOT NULL
);

CREATE TABLE IF NOT EXISTS cinemas(
    id serial PRIMARY KEY,
    created_at timestamp(0) with time zone NOT NULL DEFAULT NOW(),
    title varchar(64) NOT NULL
);

CREATE TABLE IF NOT EXISTS showtime(
    id serial PRIMARY KEY,
    created_at timestamp(0) with time zone NOT NULL DEFAULT NOW(),
    movie_id integer NOT NULL REFERENCES movies(id) ON DELETE CASCADE,
    cinema_id integer NOT NULL REFERENCES cinemas(id) ON DELETE CASCADE,
    movie_start_time timestamp(0) with time zone NOT NULL,
    movie_end_time timestamp(0) with time zone NOT NULL
);

CREATE TABLE IF NOT EXISTS seats (
    id SERIAL PRIMARY KEY,
    cinemas_id integer NOT NULL REFERENCES cinemas(id) ON DELETE CASCADE,
    seat_number integer NOT NULL
);

CREATE TABLE IF NOT EXISTS reservation (
    id SERIAL PRIMARY KEY,
    created_at timestamp(0) with time zone NOT NULL DEFAULT NOW(),
    showtime_id integer NOT NULL REFERENCES showtime(id) ON DELETE CASCADE,
    seat_id integer NOT NULL REFERENCES seats(id) ON DELETE CASCADE,
    user_id integer NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(255)
);

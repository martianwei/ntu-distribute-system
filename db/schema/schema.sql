CREATE TABLE IF NOT EXISTS users (
    id serial PRIMARY KEY,
    created_at timestamp(0) with time zone NOT NULL DEFAULT NOW(),
    username varchar(64) NOT NULL,
    email varchar(255) UNIQUE NOT NULL,
    password varchar(64) DEFAULT NULL,
    activated boolean NOT NULL,
);

CREATE TABLE IF NOT EXISTS movies(
    id serial PRIMARY KEY,
    created_at timestamp(0) with time zone NOT NULL DEFAULT NOW(),
    title varchar(64) NOT NULL,
    duration TIME,
    category varchar(64) NOT NULL,
);

CREATE TABLE IF NOT EXISTS cinemas(
    id serial PRIMARY KEY,
    created_at timestamp(0) with time zone NOT NULL DEFAULT NOW(),
    title varchar(64) NOT NULL,
    duration TIME,
    category varchar(64) NOT NULL,
);

CREATE TABLE IF NOT EXISTS showtime(
    id serial PRIMARY KEY,
    created_at timestamp(0) with time zone NOT NULL DEFAULT NOW(),
    movie_id integer FOREIGN KEY REFERENCES movies(id),
    cinema_id integer FOREIGN KEY REFERENCES cinemas(id),
    
);

CREATE TABLE IF NOT EXISTS seats (
    id SERIAL PRIMARY KEY,
    cinemas_id integer FOREIGN KEY REFERENCES cinemas(id) ,
    seat_number integer NOT NULL,
);

CREATE TABLE IF NOT EXISTS reservation (
    id SERIAL PRIMARY KEY,
    created_at timestamp(0) with time zone NOT NULL DEFAULT NOW(),
    showtime_id integer FOREIGN KEY REFERENCES showtime(id),
    seat_id integer FOREIGN KEY REFERENCES seats(id),
    user_id integer FOREIGN KEY REFERENCES users(id),
    price integer NOT NULL,
    status VARCHAR(255)
);

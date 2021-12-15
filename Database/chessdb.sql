DROP TABLE IF EXISTS users;
CREATE TABLE users (
    ix INTEGER PRIMARY KEY,
    id STRING,
    blitz_games NUMERIC,
    blitz_rating NUMERIC,
    bullet_games NUMERIC,
    bullet_rating NUMERIC,
    rapid_games NUMERIC,
    rapid_rating NUMERIC,
    country STRING
);

DROP TABLE IF EXISTS country;
CREATE TABLE country (
    id INTEGER PRIMARY KEY,
    name STRING,
    alpha2 STRING,
    alpha3 STRING
);

DROP TABLE IF EXISTS users_selected;


DROP TABLE IF EXISTS all_games_raw;

DROP TABLE IF EXISTS all_games_country;


DROP TABLE IF EXISTS all_games_country_selected;


DROP TABLE IF EXISTS all_games_countries_winstreak;

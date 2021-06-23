CREATE SCHEMA staging AUTHORIZATION test_user;

GRANT USAGE ON SCHEMA staging TO test_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA staging TO test_user;

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

CREATE TABLE staging.name_basics (
    nconst VARCHAR(10),
    primaryName VARCHAR(256),
    birthYear INTEGER,
    deathYear INTEGER,
    primaryProfession VARCHAR(256),
    knownForTitles VARCHAR(256)
);

CREATE TABLE staging.title_ratings (
    tconst VARCHAR(10),
    averageRating FLOAT,
    numVotes INTEGER
);

CREATE TABLE staging.title_crew (
    tconst VARCHAR(10),
    directors TEXT,
    writers TEXT
);

CREATE TABLE staging.title_episode (
    tconst VARCHAR(10),
    parentTconst VARCHAR(10),
    seasonNumber INTEGER,
    episodeNumber INTEGER
);

CREATE TABLE staging.title_basics (
    tconst VARCHAR(10),
    titleType VARCHAR(20),
    primaryTitle TEXT,
    originalTitle TEXT,
    isAdult BOOLEAN,
    startYear INTEGER,
    endYear INTEGER,
    runtimeMinutes INTEGER,
    genres TEXT
);

CREATE TABLE staging.title_principals (
    tconst VARCHAR(10),
    ordering INTEGER,
    nconst VARCHAR(10),
    category VARCHAR(20),
    job TEXT,
    characters TEXT
);


CREATE TABLE staging.title_akas (
    titleId VARCHAR(10),
    ordering INTEGER,
    title TEXT,
    region VARCHAR(10),
    language VARCHAR(10),
    types VARCHAR(20),
    attributes VARCHAR(256),
    isOriginalTitle BOOLEAN
);

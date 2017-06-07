-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players(id SERIAL PRIMARY KEY, name TEXT, wins INT, matches INT);

CREATE TABLE matches(id SERIAL PRIMARY KEY, winner INT REFERENCES players(id) ON DELETE CASCADE,
loser INT REFERENCES players(id) ON DELETE CASCADE,
CHECK (winner <> loser));

CREATE VIEW standing AS
    SELECT id,
           name,
           (SELECT COUNT(*) FROM matches
                WHERE players.id = matches.winner) AS wins,
           (SELECT COUNT(*) FROM matches
                WHERE players.id IN (matches.winner, matches.loser)) AS total_matches
    FROM players
    GROUP by id;+


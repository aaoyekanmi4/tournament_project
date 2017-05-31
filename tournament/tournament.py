#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    conn = connect()
    c = conn.cursor()
    c.execute("Update players set matches = 0")
    c.execute("Update players set wins = 0")
    c.execute("Delete from matches;")
    conn.commit()
    conn.close()


def deletePlayers():
    conn = connect()
    c = conn.cursor()
    c.execute("Delete from players;")
    conn.commit()
    conn.close()



def countPlayers():
    conn = connect()
    c = conn.cursor()
    c.execute("Select count(*) from players;")
    player_count = c.fetchone()[0]
    return player_count



# add row to player table with new name

def registerPlayer(name):
    conn = connect()
    c = conn.cursor()
    c.execute("Insert into players (name, wins, matches) values (%s, 0, 0)", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    conn = connect()
    c = conn.cursor()
    c.execute("Select * from players order by wins desc;")
    standings = c.fetchall()
    conn.close()
    return standings


# record winner and loser in matches table
# record one more match for each player in players table
# increase winner's win count by 1


def reportMatch(winner, loser):
    conn = connect()
    c = conn.cursor()

    c.execute("Insert into matches (winner, loser) values (%s, %s)", (winner, loser))
    c.execute("Update players set matches = matches + 1 where id = (%s)", (winner,))
    c.execute("Update players set matches = matches + 1 where id = (%s)", (loser,))
    c.execute("Update players set wins = wins + 1 where id = (%s)", (winner,))
    conn.commit()
    conn.close()


def countMatches():
    conn = connect()
    c = conn.cursor()
    c.execute("Select count(*) from matches;")
    match_count = c.fetchone()[0]
    return match_count


# pair off all players in the list

def initial_pairing(even_list):
    x = 0
    pairs = []
    for i in range (len(even_list)/2):
        pairs.append(even_list[x] + even_list[x+1])
        x += 2
    return pairs



def swissPairings():
    conn = connect()

    c = conn.cursor()
    match_count = countMatches()

    # pair players at the beginning
    if match_count == 0:
        c.execute("Select id, name from players")
        player_list = c.fetchall()
        pairs = initial_pairing(player_list)

    # pair up players with equal wins and matches if a match has been played
    else:
        player_count = countPlayers()
        n_pair = (player_count/2)

        c.execute("""Select a.id, a.name, b.id, b.name from players a, players b where
        a.wins = b.wins and a.matches = b.matches and a.id > b.id limit (%s)""", (n_pair,))
        pairs = c.fetchall()

    conn.close()
    return pairs

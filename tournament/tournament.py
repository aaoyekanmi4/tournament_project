#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
# Written for Udacity fullstack nanodegree program.

import psycopg2

# Connect to database and get cursor

def connect(database_name="tournament"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Unable to access database")

# Delete match from matches table and players table
def deleteMatches():
    db, cursor = connect()
    cursor.execute("UPDATE players SET matches = 0")
    cursor.execute("UPDATE players SET wins = 0")
    cursor.execute("DELETE FROM matches;")
    db.commit()
    db.close()

# Deleting a player by removing a row from the player's table
def deletePlayers():
    db, cursor = connect()
    cursor.execute("Delete from players;")
    db.commit()
    db.close()


# Count players by counting rows
def countPlayers():
    db, cursor = connect()
    cursor.execute("SELECT count(*) FROM players;")
    player_count = cursor.fetchone()[0]
    return player_count



# Add row to player table with new name

def registerPlayer(name):
    db, cursor = connect()
    query = "INSERT INTO players (name, wins, matches) VALUES (%s, 0, 0)"
    paramater = (name,)
    cursor.execute(query, paramater)
    db.commit()
    db.close()

# Get standings by arranging player table rows from most wins to least

def playerStandings():
    db, cursor = connect()
    cursor.execute("SELECT * FROM standing ORDER BY wins DESC;")
    standings = cursor.fetchall()
    db.close()
    return standings


# Record winner and loser in matches table(first query)
# Record one more match for each player in players table(second and third queries)
# Increase winner's win count by 1(last query)

def reportMatch(winner, loser):
    db, cursor = connect()

    query = "INSERT INTO matches (winner, loser) VALUES (%s, %s)"
    parameters = (winner, loser)
    cursor.execute(query, parameters)


    query = "UPDATE players SET matches = matches + 1 WHERE id = (%s)"
    parameter = (winner,)
    cursor.execute(query, parameter)

    query = "UPDATE players SET matches = matches + 1 WHERE id = (%s)"
    parameter = (loser,)
    cursor.execute(query, parameter)


    query = "UPDATE players SET wins = wins + 1 WHERE id = (%s)"
    parameter = (winner,)
    cursor.execute(query, parameter)

    db.commit()
    db.close()

# Count number of rows in matches table

def countMatches():
    db, cursor = connect()
    cursor.execute("SELECT count(*) FROM matches;")
    match_count = cursor.fetchone()[0]
    db.close()
    return match_count


# Pair off all players in the list before any matches played

def initial_pairing(even_list):
    x = 0
    pairs = []
    for i in range (len(even_list)/2):
        pairs.append(even_list[x] + even_list[x+1])
        x += 2
    return pairs


#Create match ups of players if their win and match counts are the same

def swissPairings():
    db, cursor = connect()
    match_count = countMatches()

    # Pair players at the beginning using initial_pairings
    if match_count == 0:
        cursor.execute("SELECT id, name FROM players")
        player_list = cursor.fetchall()
        pairs = initial_pairing(player_list)

    # Get number of pairs (n_pair) of players by dividing player_count by 2
    else:
        player_count = countPlayers()
        n_pair = (player_count/2)

    # Select two players where number of wins and matches are equal for the number of pairs that exist
        cursor.execute("""SELECT a.id, a.name, b.id, b.name FROM players a, players b WHERE
        a.wins = b.wins AND a.matches = b.matches AND a.id > b.id LIMIT (%s)""", (n_pair,))
        pairs = cursor.fetchall()

    db.close()
    return pairs

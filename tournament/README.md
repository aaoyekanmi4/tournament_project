# Tournament Database Project README

## To Run:

1. Download [Virtual Box](https://www.virtualbox.org/wiki/Downloads)

2. Download [Vagrant](https://www.vagrantup.com/downloads.html)

3. Clone this repository onto your system

4. Navigate to the directory where you cloned the files

5. Run vagrant up to boot up the virtual machine

6. Run vagrant ssh to log in

7. Navigate to shared files by using cd /vagrant

8. Navigate to tournament folder

9. Run command psql to start postgresql

10. Run command \i tournament.sql to make database and tables

11. Exit psql with \q

12. Run command python tournament_test.py in tournament
folder to populate database and test functions.

## About:

This was a project in the Udacity Full Stack Nanodegree program.
We learned how to create, modify, and query relational databases.

For this project, we created a database using psql in order to
create swiss pairings for tournaments with an even number of players.

- The tournament.py file uses Python's DB-API to connect to a postgresql database
and run functions in order to update and query the tables. The resulting information is used
to form swiss pairings in the function with that name.

- The tournament.sql file contains the commands for postgresql to create a database
with the tables necessary for the tournament.py file.

- The tournament_test.py is a test suite created by udacity for the functions formed in tournament.py

The files which I modified in the project are tournament.py and tournament.sql.

## Acknowledgements

Udacity class [Intro to Relational Databases](https://www.udacity.com/course/intro-to-relational-databases--ud197) for the files and configurations necessary to run tournament.py and to test it.

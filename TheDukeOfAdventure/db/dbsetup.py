import sqlite3 as sql
import os

con = None
databaseName = "test.db"

def testDB():
    pass

if __name__ == "__main__":

    # Try to remove the database file if it already exists.
    #TODO: In the future, maybe make command line argument
    #      like "clean" for this.
    try:
        os.remove(databaseName)
    except OSError:
        print("File {0} does not exist, skipping...".format(databaseName))

    con = sql.connect(databaseName)
    cur = con.cursor()

    # Build Users
    queryString = """CREATE TABLE IF NOT EXISTS Players (
                        user_id VARCHAR(64) NOT NULL PRIMARY KEY,
                        nickname VARCHAR(255) NOT NULL
                     );"""

    cur.execute(queryString);

    # Build Characters table
    queryString = """CREATE TABLE IF NOT EXISTS Characters (
                        owner_id VARCHAR(64) NOT NULL,
                        level INTEGER NOT NULL DEFAULT 1,
                        stat_points INTEGER NOT NULL,
                        max_hp INTEGER NOT NULL,
                        current_hp INTEGER NOT NULL,
                        fight INTEGER NOT NULL,
                        body INTEGER NOT NULL,
                        spirit INTEGER NOT NULL,
                        FOREIGN KEY (owner_id) REFERENCES Players (user_id)
                     );"""

    cur.execute(queryString);

    #Build Inventories table
    queryString = """CREATE TABLE IF NOT EXISTS Inventories (
                        owner_id VARCHAR(64) NOT NULL,
                        gold INTEGER NOT NULL default 0,
                        FOREIGN KEY (owner_id) REFERENCES Players (user_id)
                     );"""

    cur.execute(queryString);

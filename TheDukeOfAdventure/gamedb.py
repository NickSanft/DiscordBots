import sqlite3 as sql

dbPath = "db/game.db"
con = None

###############################################################
# Initialize the database connection
def init():
    global con
    con = sql.connect(dbPath)

    print("Connected to database at {0}".format(dbPath))

# Perform a SELECT on a table to make sure that the
# connection is good.
# TODO: Is this even needed? Check docs
def test_select():
    cur = con.cursor()
    queryString = """SELECT * FROM Characters"""

    try:
        cur.execute(queryString)
    except:
        print("Something went wrong with the SELECT")

init()
test_select()
###############################################################

# Returns the name and level of every character
def getAllCharacters():

    cur = con.cursor()

    queryString = "SELECT * FROM Characters ORDER BY name ASC"
    cur.execute(queryString)
    data = cur.fetchall()

    return data

# Writes the list to the database of characters.
def saveAll(listOfCharacters):

    cur = con.cursor()

    queryString = "INSERT OR REPLACE INTO Characters VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
    cur.executemany(queryString, listOfCharacters)
    con.commit()

# Check if a character already exists belonging to the player
# specified by id.
def player_exists(id: str):
    cur = con.cursor()

    queryString = "SELECT * FROM Characters WHERE user_id=?"
    cur.execute(queryString, (id,))
    data = cur.fetchone()

    if data == None:
        return False

    return True

# Returns the ID of the owner of a character given the name.
def whois(name: str):

    cur = con.cursor()

    queryString = "SELECT user_id FROM Characters WHERE name=?"

    cur.execute(queryString, (name,))
    data = cur.fetchone()

    return data

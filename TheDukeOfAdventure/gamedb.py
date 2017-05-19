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

# Adds a new character to the game using a discord id.
def add_character(id: str, name: str):

    if player_exists(id):
        print("Character already exists belonging to user id {0}".format(id))
        return False
    else:
        cur = con.cursor()

        queryString = """INSERT OR REPLACE INTO Characters (user_id, name)
                         VALUES (?, ?)"""

        cur.execute(queryString, (id, name))
        data = cur.fetchone()

        print("Inserted data: {0}".format(data))

        con.commit()

        return True

# Updates a character's name.
def update_name(id: str, name: str):

    if player_exists(id):
        cur = con.cursor()

        queryString = "UPDATE Characters SET name=? WHERE user_id=?"

        cur.execute(queryString, (name, id))
        data = cur.fetchone()

        print("Inserted data: {0}".format(data))

        con.commit()

        return True
    else:
        return False

# Returns the row of a character.
# TODO: And their inventory.
def get_character(id: str):

    cur = con.cursor()

    queryString = "SELECT * FROM Characters WHERE user_id=?"

    cur.execute(queryString, (id,))
    data = cur.fetchone()

    return data

# Returns the ID of the owner of a character given the name.
def whois(name: str):

    cur = con.cursor()

    queryString = "SELECT user_id FROM Characters WHERE name=?"

    cur.execute(queryString, (name,))
    data = cur.fetchone()

    return data

# Returns the name and level of every character
def get_all_characters():

    cur = con.cursor()

    queryString = "SELECT name, level FROM Characters ORDER BY name ASC"

    cur.execute(queryString)
    data = cur.fetchall()

    return data

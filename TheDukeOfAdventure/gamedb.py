import sqlite3 as sql

dbPath = "db/game.db"
con = None

###############################################################
# Initialize the database connection
def init():
    global con
    con = sql.connect(dbPath)

    print("Connected to database at {0}".format(dbPath))
    print("Con object: {0}".format(con))

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

    queryString = """SELECT * FROM Characters WHERE user_id=?"""
    cur.execute(queryString, (id,))
    data = cur.fetchone()

    if data == None:
        return False

    return True

# Adds a new character to the game using a discord id.
# TODO: Don't add a user without a character.
def add_character(id: str):

    if player_exists(id):
        print("Character already exists belonging to user id {0}".format(id))
    else:
        cur = con.cursor()

        queryString = """INSERT OR REPLACE INTO Characters (user_id)
                         VALUES (?)"""

        cur.execute(queryString, (id,))
        data = cur.fetchone()

        print("Inserted data: {0}".format(data))

        con.commit()

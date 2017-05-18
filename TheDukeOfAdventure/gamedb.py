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
    queryString = """SELECT * FROM Players"""

    try:
        cur.execute(queryString)
    except:
        print("Something went wrong with the SELECT")

init()
test_select()
###############################################################

# Adds a user to the game with their discord user id and server nickname.
# TODO: Don't add a user without a character.
def add_user(id: str, nickname: str):
    cur = con.cursor()

    queryString = """INSERT OR REPLACE INTO Players (user_id, nickname)
                     VALUES (?, ?)"""

    cur.execute(queryString, (id, nickname))
    data = cur.fetchone()

    print("Inserted data: {0}".format(data))

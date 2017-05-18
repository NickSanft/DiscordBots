import sqlite3 as sql

databaseName = "skeleton.db"
con = sql.connect(databaseName)

#run this for initial db setup or if a schema change has been made and you want to wipe everything.
def initDataBase():
    dropTables()
    createTables()


def dropTables():
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for row in cur:
        query = "DROP TABLE IF EXISTS " + row[0]
        print(query)
        con.cursor().execute(query)
        con.commit()

def createTables():
    con.cursor().execute('''CREATE TABLE IF NOT EXISTS GW2_API_KEYS
    (DiscordID varchar(100) PRIMARY KEY, DiscordName varchar(100), GWAPIKey varchar(200), insertDate datetime)''')
    con.cursor().execute('''CREATE TABLE IF NOT EXISTS continents (ItemID INTEGER PRIMARY KEY, ItemDescription varchar(200))''')
    con.cursor().execute('''CREATE TABLE IF NOT EXISTS currencies (ItemID INTEGER PRIMARY KEY, ItemDescription varchar(200))''')
    con.cursor().execute('''CREATE TABLE IF NOT EXISTS items (ItemID INTEGER PRIMARY KEY, ItemDescription varchar(200))''')
    con.commit()

def cleanTables():
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for row in cur:
        con.cursor().execute("DELETE FROM " + row[0])
        con.commit() 
           

"""
def insertTest():
    cur = con.cursor()
    cur.execute("INSERT INTO GW2_API_KEYS VALUES ('123567777','1234',date('now'))")
    con.commit()
"""

def insertQuery(tableName, itemID, itemDescription):
    con.cursor().execute("INSERT INTO " + tableName + " VALUES (?,?)",(itemID,itemDescription))
    con.commit()
    

def getAPIKey(DiscordID):
    cur = con.cursor()
    cur.execute("SELECT GWAPIKey FROM GW2_API_KEYS WHERE DiscordID = ?",(DiscordID,))
    return cur.fetchone()[0]

def registerAPIKey(DiscordID,DiscordName,APIKey):
    cur = con.cursor()
    cur.execute("REPLACE INTO GW2_API_KEYS VALUES (?,?,?,date('now'))",(DiscordID,DiscordName,APIKey))
    con.commit()

def selectAllQuery(tableName):
    cur = con.cursor()
    cur.execute("SELECT * FROM " + tableName)
    data = cur.fetchall()
    return data

def countQuery(tableName):
    cur = con.cursor().execute("SELECT COUNT(1) FROM " + tableName)
    return cur.fetchone()[0]
    

#createTables()
#print(countQuery("continents"))
#initDataBase()
#insertTest()
#cleanTables()
#print(selectTest())
#con.commit()

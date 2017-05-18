import sqlite3 as sql

con = sql.connect('test.db')

def initDataBase():
    con.cursor().execute('''DROP TABLE IF EXISTS GW2_API_KEYS''')
    con.cursor().execute('''CREATE TABLE IF NOT EXISTS GW2_API_KEYS
             (DiscordID varchar(100) PRIMARY KEY, DiscordName varchar(100), GWAPIKey varchar(200), insertDate datetime)''')

def dropTable():
    con.cursor().execute('''DROP TABLE IF EXISTS GW2_API_KEYS''')

def cleanTables():
    con.cursor().execute('''DELETE FROM GW2_API_KEYS''')

def insertTest():
    cur = con.cursor()
    cur.execute("INSERT INTO GW2_API_KEYS VALUES ('123567777','1234',date('now'))")
    con.commit()

def getAPIKey(DiscordID):
    cur = con.cursor()
    cur.execute("SELECT GWAPIKey FROM GW2_API_KEYS WHERE DiscordID = ?",(DiscordID,))
    return cur.fetchone()[0]

def registerAPIKey(DiscordID,DiscordName,APIKey):
    cur = con.cursor()
    cur.execute("REPLACE INTO GW2_API_KEYS VALUES (?,?,?,date('now'))",(DiscordID,DiscordName,APIKey))
    con.commit()

def selectTest():
    return sql_query("SELECT * FROM GW2_API_KEYS")

def sql_query(query):
    cur = con.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return data

#dropTable()
#initDataBase()
#insertTest()
#cleanTables()
print(selectTest())
#con.commit()

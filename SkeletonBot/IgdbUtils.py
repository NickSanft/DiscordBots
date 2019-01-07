from igdb_api_python.igdb import igdb
import datetime
import time
import json

def getGames():
    gamesDict = {}
    gameNamesDict = {}
    platformsList = []
    platformsDict = {}
    igdbObject = igdb('eac2eee6829a92ef324ce05ed6410039')

    today = int(round(time.time() * 1000))
    nextWeek = today + 604800000


    #getting our released games...
    gamesObject = igdbObject.release_dates({
        'limit':50,
        'filters' :{"[date][gt]": today,"[date][lt]": nextWeek},
            'order':"date:asc",
            'fields':['game','platform','date']
            })

    for item in gamesObject.json():
        platform = str(item.get('platform'))
        gamesDict[str(item.get('game'))] = (platform, secondsToDate(item.get('date') / 1000))
        if platform not in platformsList:
            platformsList.append(platform)
    print(json.dumps(gamesObject.json()))
    #getting the names of our released games...
    gameNamesResponse = igdbObject.games({'ids': list(gamesDict.keys()),'fields':['id','name']})
    for gameName in gameNamesResponse.json():
        gameNamesDict[str(gameName.get('id'))] = (gameName.get('name'))
    #getting the platform names of our released games...
    platformsResponse = igdbObject.platforms({'ids': platformsList,'fields':['id','name']})
    for platform in platformsResponse.json():
        platformsDict[str(platform.get('id'))] = (platform.get('name'))
    #bringing it all together...
    resultString = "```Here are the known games releasing next week: \n"
    for gameID, dataTuple in gamesDict.items():
        resultString += "Game Name: " + gameNamesDict[gameID]
        resultString += " Platform: " + platformsDict[dataTuple[0]]
        resultString += " Release Date: " + dataTuple[1] + "\n"
    resultString += "```"

    return resultString

def secondsToDate(ms):
    return datetime.datetime.fromtimestamp(ms).strftime('%Y-%m-%d')    

def main():
    print(getGames())

if __name__ == '__main__':
    main()            
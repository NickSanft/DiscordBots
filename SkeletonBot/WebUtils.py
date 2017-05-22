import requests, bs4, json, DataBaseUtils

gw2_api_url = "https://api.guildwars2.com/v2/"

def loadItems():
    itemJSON = json.loads(str(getSoup(gw2_api_url + "items")))
    for item in itemJSON:
        key = str(item)
        if DataBaseUtils.hasItem(key):
           print(key + " already exists!")
        else:
            itemSoup = json.loads(str(getSoup(gw2_api_url + "items?id=" + key)))
            DataBaseUtils.insertQuery("items",item,itemSoup.get('name'))

def getSoup(url):
    try:
        print('Downloading page %s...' % url)
        res = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
        res.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return None
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    return soup

def getGW2ApiData(functionName):
    url = gw2_api_url + functionName
    soup = getSoup(url)
    itemJSON = json.loads(str(soup))
    print(itemJSON)
    results = {}
    for item in itemJSON:
        key = str(item)
        itemSoup = json.loads(str(getSoup(url + "?id=" + key)))
        DataBaseUtils.insertQuery(functionName,item,itemSoup.get('name'))

def getAccountData(DiscordID):
    APIKey = DataBaseUtils.getAPIKey(DiscordID)
    return getSoup(gw2_api_url + "account?access_token=" + APIKey)
        
def getWorld(DiscordID):
    world = json.loads(str(getAccountData(DiscordID))).get('world')
    return json.loads(str(getSoup(gw2_api_url + "worlds?id=" + str(world)))).get('name')

def getCharacters(DiscordID):
    APIKey = DataBaseUtils.getAPIKey(DiscordID)
    return json.loads(str(getSoup(gw2_api_url + "characters?access_token=" + str(APIKey))))
                          
def getDisplayName(DiscordID):
    return json.loads(str(getAccountData(DiscordID))).get('name')

def getRemainingAP(DiscordID):
    accountJSON = json.loads(str(getAccountData(DiscordID)))
    result = 15000 - (int(accountJSON.get('daily_ap')) + int(accountJSON.get('monthly_ap')))
    if(result < 15000):
        text = "You have " + str(result) + " remaining. Only " + str(result/10) + " more days before the nightmare ends!"
    else:
        text = "YOU ARE FREE FROM THE NIGHTMARE"
    return text

def getGWWikiHTML(query):
    result = getSoup("https://wiki.guildwars2.com/wiki/" + query.replace(" ","_"))
    if result == None:
        return "an error occurred getting your query, boss: " + query
    return result.select("p")[0].getText() + "\n" + result.select("p")[1].getText()


def gw2Exchange(currencyType, quantity):
    return getSoup(gw2_api_url + 'commerce/exchange/'+ currencyType + '?quantity='+ quantity)

#loadItems()

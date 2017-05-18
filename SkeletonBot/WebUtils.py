import requests, bs4, json, DataBaseUtils

continentsDict = {}
currenciesDict = {}

gw2_api_url = "https://api.guildwars2.com/v2/"

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
    print(eval(functionName + "Dict"))
    url = gw2_api_url + functionName
    soup = getSoup(url)
    itemJSON = json.loads(str(soup))
    print(itemJSON)
    results = {}
    for item in itemJSON:
        key = str(item)
        if key not in eval(functionName + "Dict"):
            print("Did not have id: " + key)
            itemSoup = json.loads(str(getSoup(url + "?id=" + key)))
            eval(functionName + "Dict")[str(item)] = itemSoup.get('name')
    return getDictByName(functionName)

def getDisplayName(DiscordID):
    APIKey = DataBaseUtils.getAPIKey(DiscordID)
    soup = getSoup(gw2_api_url + "account?access_token=" + APIKey)
    nameJSON = json.loads(str(soup))
    #print(soup)
    return nameJSON.get('name')
    
def getDictByName(functionName):
    return eval(functionName + "Dict")


def getGWWikiHTML(query):
    result = getSoup("https://wiki.guildwars2.com/wiki/" + query.replace(" ","_"))
    if result == None:
        return "an error occurred getting your query, boss: " + query
    return result.select("p")[0].getText() + "\n" + result.select("p")[1].getText()



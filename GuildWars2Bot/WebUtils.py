import requests, bs4, json, DataBaseUtils

gw2_api_url = "https://api.guildwars2.com/v2/"

"""
This is a simple decorator to wrap a result in "```" characters to nicely
format text when sending back a message from the bot.
"""
def make_pretty(func):
   def func_wrapper(name):
       return "```{0}```".format(func(name))
   return func_wrapper

def loadItems():
    itemJSON = json.loads(str(getSoup(gw2_api_url + "items")))
    for item in itemJSON:
        key = str(item)
        if DataBaseUtils.hasItem(key):
           print(key + " already exists!")
        else:
            itemSoup = json.loads(getSoup(gw2_api_url + "items?id=" + key).text)
            DataBaseUtils.insertQuery("items",item,itemSoup.get('name'))

"""
This is a generic helper method that can be used to get the response from a URL
as a soup object.
"""
def getSoup(url):
    try:
        print('Downloading page %s...' % url)
        res = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
        res.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return None
    except requests.exceptions.ConnectionError as err:
        return getSoup(url)    
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
        itemSoup = json.loads(getSoup(url + "?id=" + key).text)
        DataBaseUtils.insertQuery(functionName,item,itemSoup.get('name'))

@make_pretty
def getItemPrice(name):
    data = DataBaseUtils.findItemByName(name)
    if(len(data) > 10):
        return "Too many results (got " + str(len(data)) +  ", max is 10)! Please refine your search."
    elif(len(data) < 1):
         return "No results! Please refine your search."
    results = ""
    for item in data:
        key = str(item[0])
        url = gw2_api_url + "commerce/prices?id=" + key
        soup = getSoup(url)
        results += "Item ID: " + key + "\n"
        results += "Item Description: " + item[1] + "\n"
        if soup == None:
            results += "Could not find on the Trading Post! This item is probably untradeable... \n\n"
        else:
            itemJSON = json.loads(soup.text)
            results += "Buy price: " + str(itemJSON.get('buys').get('unit_price') / 10000) + " gold \n"
            results += "Sell price: " + str(itemJSON.get('sells').get('unit_price') / 10000) + " gold \n\n"
    return results

@make_pretty
def getItemInfoByName(name):
    data = DataBaseUtils.findItemByName(name)
    if(len(data) > 10):
        return "Too many results (got " + str(len(data)) +  ", max is 10)! Please refine your search."
    elif(len(data) < 1):
         return "No results! Please refine your search."         
    results = ""
    for item in data:
        key = str(item[0])
        #url = gw2_api_url + "items?id=" + key
        #itemPicture = json.loads(getSoup(url).text).get('icon')
        results += key + ": " + item[1] + "\n"
    return results

def getAccountData(DiscordID):
    APIKey = DataBaseUtils.getAPIKey(DiscordID)
    return getSoup(gw2_api_url + "account?access_token=" + APIKey)

@make_pretty
def getWorld(DiscordID):
    world = json.loads(getAccountData(DiscordID).text).get('world')
    return json.loads(getSoup(gw2_api_url + "worlds?id=" + str(world)).text).get('name')

@make_pretty
def getCharacters(DiscordID):
    results = ""
    APIKey = DataBaseUtils.getAPIKey(DiscordID)
    characterJSON = json.loads(getSoup(gw2_api_url + "characters?access_token=" + str(APIKey)).text)
    for character in characterJSON:
        results += character + "\n"
    return results
     
@make_pretty                          
def getDisplayName(DiscordID):
    return "Your account name is: " + json.loads(str(getAccountData(DiscordID))).get('name')

@make_pretty
def getRemainingAP(DiscordID):
    accountJSON = json.loads(getAccountData(DiscordID).text)
    result = 15000 - (int(accountJSON.get('daily_ap')) + int(accountJSON.get('monthly_ap')))
    if(result < 15000):
        text = "You have " + str(result) + " remaining. Only " + str(result/10) + " more days before the nightmare ends!"
    else:
        text = "YOU ARE FREE FROM THE NIGHTMARE"
    return text

@make_pretty
def getGWWikiHTML(query):
    result = getSoup("https://wiki.guildwars2.com/wiki/" + query.replace(" ","_"))
    if result == None:
        return "an error occurred getting your query, boss: " + query
    return result.select("p")[0].getText() + "\n" + result.select("p")[1].getText()

@make_pretty
def gw2Exchange(currencyType, quantity):
    return getSoup(gw2_api_url + 'commerce/exchange/'+ currencyType + '?quantity='+ quantity)

#loadItems()
#getItemInfoByName("Jalis")

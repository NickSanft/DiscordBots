import requests, bs4, json, DataBaseUtils, aiohttp
from collections import defaultdict

gw2_api_url = "https://api.guildwars2.com/v2/"
maxItems = 30

"""
This is a simple decorator to wrap a result in "```" characters to nicely
format text when sending back a message from the bot.
"""
def make_pretty(func):
   async def func_wrapper(*args, **kwargs):
       return "```{0}```".format(await func(*args, **kwargs))
   return func_wrapper

def loadItems():
    itemJSON = getJSON(gw2_api_url + "items")
    for item in itemJSON:
        key = str(item)
        if DataBaseUtils.hasItem(key):
           print(key + " already exists!")
        else:
            itemSoup = getJSON(gw2_api_url + "items?id=" + key)
            DataBaseUtils.insertQuery("items",item,itemSoup.get('name'))

async def getJSON(url):
   async with aiohttp.get(url) as r:
      if r.status == 200:
         js = await r.json()
         return js
    

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
        return (url)    
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    return soup

async def getGW2ApiData(functionName):
    url = gw2_api_url + functionName
    soup = await getJSON(url)
    itemJSON = json.loads(str(soup))
    print(itemJSON)
    results = {}
    for item in itemJSON:
        key = str(item)
        itemSoup = json.loads(getJSON(url + "?id=" + key).text)
        DataBaseUtils.insertQuery(functionName,item,itemSoup.get('name'))

@make_pretty
async def getItemPrice(name):
    data = DataBaseUtils.findItemByName(name)
    
    if(len(data) > maxItems):
        return "Too many results (got " + str(len(data)) +  ", max is " + str(maxItems) + ")! Please refine your search."
    elif(len(data) < 1):
         return "No results! Please refine your search."
    results = ""
    for item in data:
        key = str(item[0])
        url = gw2_api_url + "commerce/prices?id=" + key
        itemJSON = await getJSON(url)
        if itemJSON == None:
            results += "Could not find on the Trading Post! This item is probably untradeable... \n\n"
        else:
            results += "Item ID: " + key + "\n"
            results += "Item Description: " + item[1] + "\n"
            results += "Buy price: " + str(itemJSON.get('buys').get('unit_price') / 10000) + " gold \n"
            results += "Sell price: " + str(itemJSON.get('sells').get('unit_price') / 10000) + " gold \n\n"
    return results

@make_pretty
async def getItemInfoByName(name):
    data = DataBaseUtils.findItemByName(name)
    if(len(data) > maxItems):
        return "Too many results (got " + str(len(data)) +  ", max is " + str(maxItems) + ")! Please refine your search."
    elif(len(data) < 1):
         return "No results! Please refine your search."      
    results = ""
    for item in data:
        key = str(item[0])
        #url = gw2_api_url + "items?id=" + key
        #itemPicture = json.loads(getJSON(url).text).get('icon')
        results += key + ": " + item[1] + "\n"
    return results

#TODO figure out how to better refactor this...
@make_pretty
async def getBankCount(DiscordID, name):
    APIKey = DataBaseUtils.getAPIKey(DiscordID)
    data = DataBaseUtils.findItemByName(name)
    if(len(data) > maxItems):
        return "Too many results (got " + str(len(data)) +  ", max is " + str(maxItems) + ")! Please refine your search."
    elif(len(data) < 1):
         return "No results! Please refine your search."     
    itemDict = {}
    for item in data:
       itemDict[item[0]] = (item[1],0)
    url = gw2_api_url + "account/bank?access_token=" + APIKey
    bankItems = await getJSON(url)
    for item in bankItems:
       if item is None:
          continue
       itemID = item.get('id')
       if itemID in itemDict:
          old_value = itemDict[itemID]
          new_value = old_value[0],old_value[1] + item.get('count')
          itemDict[itemID] = new_value
    results = "Here is a list of how many of each item you have in your bank... \n"          
    for item in itemDict:
       value = itemDict[item]
       results += "ItemID: " + str(item) + "\n"
       results += "ItemDescription: " + value[0] + "\n"
       results += "ItemCount: " + str(value[1]) + "\n\n"
    return results

@make_pretty
async def getMaterials(DiscordID, ItemName):
    data = DataBaseUtils.findItemByName(ItemName)
    print(data)
    if(len(data) > maxItems):
        return "Too many results (got " + str(len(data)) +  ", max is " + str(maxItems) + ")! Please refine your search."
    elif(len(data) < 1):
         return "No results! Please refine your search."
    APIKey = DataBaseUtils.getAPIKey(DiscordID)
    AccessToken = "?access_token=" + str(APIKey)
    itemDict = {}
    for item in data:
       itemDict[item[0]] = (item[1],0)    
    itemJSON = await getJSON(gw2_api_url + "account/materials" + AccessToken)     
    for item in itemJSON:
       if item is None:
         continue
       itemID = item.get('id')
       if itemID in itemDict:
            old_value = itemDict[itemID]
            new_value = old_value[0],old_value[1] + item.get('count')
            itemDict[itemID] = new_value

    results = "Here is a list of how many of each item you have in your material storage... \n"          
    for item in itemDict:
       value = itemDict[item]
       results += "ItemID: " + str(item) + "\n"
       results += "ItemDescription: " + value[0] + "\n"
       results += "ItemCount: " + str(value[1]) + "\n\n"
    return results     

#TODO Refactor this with getCharacters
@make_pretty
async def getWallet(DiscordID, currencyName):
    if currencyName is not None:
       data = DataBaseUtils.findCurrencyByName(currencyName)
       if(len(data) < 1):
          return "No results! Please refine your search."
    else:
       data = DataBaseUtils.selectAllQuery("currencies")
    APIKey = DataBaseUtils.getAPIKey(DiscordID)
    AccessToken = "?access_token=" + str(APIKey)
    itemDict = {}
    for item in data:
       itemDict[item[0]] = (item[1],0)    
    itemJSON = await getJSON(gw2_api_url + "account/wallet" + AccessToken)      
    for item in itemJSON:
       if item is None:
         continue
       itemID = item.get('id')
       if itemID in itemDict:
            old_value = itemDict[itemID]
            new_value = old_value[0],old_value[1] + item.get('value')
            itemDict[itemID] = new_value
    results = "Here are the amounts of your requested currencies... \n"          
    for item in itemDict:
       value = itemDict[item]
       results += "ItemID: " + str(item) + "\n"
       results += "ItemDescription: " + value[0] + "\n"
       results += "ItemCount: " + str(value[1]) + "\n\n"
    return results  

#TODO Refactor this with getCharacters
@make_pretty
async def getCharacterInventory(DiscordID, ItemName):
    data = DataBaseUtils.findItemByName(ItemName)
    if(len(data) > maxItems):
        return "Too many results (got " + str(len(data)) +  ", max is " + str(maxItems) + ")! Please refine your search."
    elif(len(data) < 1):
         return "No results! Please refine your search."
    APIKey = DataBaseUtils.getAPIKey(DiscordID)
    AccessToken = "?access_token=" + str(APIKey)
    itemDict = {}
    for item in data:
       itemDict[item[0]] = (item[1],0)    
    characterJSON = await getJSON(gw2_api_url + "characters" + AccessToken)      
    for character in characterJSON:
        characterInv = await getJSON(gw2_api_url + "characters/" + character + "/inventory" + AccessToken)
        for bag in characterInv.get('bags'):
           if bag is None:
              continue
           for item in bag.get('inventory'):
               if item is None:
                  continue
               itemID = item.get('id')
               if itemID in itemDict:
                  old_value = itemDict[itemID]
                  new_value = old_value[0],old_value[1] + item.get('count')
                  itemDict[itemID] = new_value
    results = "Here is a list of how many of each item you have in your character inventories... \n"          
    for item in itemDict:
       value = itemDict[item]
       results += "ItemID: " + str(item) + "\n"
       results += "ItemDescription: " + value[0] + "\n"
       results += "ItemCount: " + str(value[1]) + "\n\n"
    return results

@make_pretty
async def getHeroPoints(DiscordID, charname):
    APIKey = DataBaseUtils.getAPIKey(DiscordID)
    AccessToken = "?access_token=" + str(APIKey)
    HeroPointDict = {}
    print(charname)
    if charname is None:
       characterJSON = await getJSON(gw2_api_url + "characters" + AccessToken)      
       for character in characterJSON:
          characterHP = await getJSON(gw2_api_url + "characters/" + character + "/heropoints" + AccessToken)
          HeroPointDict[character] = len(characterHP)
          results = "Here is a list of how many of Hero Points you have on each character... \n"
    else:
       characterJSON = await getJSON(gw2_api_url + "characters/" + charname + "/heropoints" + AccessToken)
       if characterJSON is not None:
          HeroPointDict[charname] = len(characterJSON)
          results = "Here are how many Hero Points you have on " + charname + "... \n"
       else:
          return "Could not find the character: " + charname + "... Did you get the name wrong?"
    
    #print(HeroPointDict)
    for character in HeroPointDict:
       value = HeroPointDict[character]
       results += "Character: " + str(character) + "\n"
       results += "Hero Points: " + str(value) + "\n\n"
    return results   
    
@make_pretty
async def getSkins(DiscordID):
    APIKey = DataBaseUtils.getAPIKey(DiscordID)
    AccessToken = "?access_token=" + str(APIKey)
    skinJSON = await getJSON(gw2_api_url + "skins/" + AccessToken)
    results = "You have: " + str(len(skinJSON)) + " skins unlocked on your account."
    return results           

async def getAccountData(DiscordID):
    APIKey = DataBaseUtils.getAPIKey(DiscordID)
    result = await getJSON(gw2_api_url + "account?access_token=" + APIKey)
    return result

@make_pretty
async def getWorld(DiscordID):
    world = await getAccountData(DiscordID)
    worldJSON = await getJSON(gw2_api_url + "worlds?id=" + str(world.get('world')))
    result = "Your world is: " + worldJSON.get('name')
    return result

@make_pretty
async def getCharacters(DiscordID):
    results = "Here is a list of your characters: \n"
    APIKey = DataBaseUtils.getAPIKey(DiscordID)
    characterJSON = await getJSON(gw2_api_url + "characters?access_token=" + APIKey)
    for character in characterJSON:
        results += character + "\n"
    return results

@make_pretty
async def getCats(DiscordID):
    results = "Here is a list of your cats: \n"
    APIKey = DataBaseUtils.getAPIKey(DiscordID)
    catJSON = await getJSON(gw2_api_url + "account/home/cats?access_token=" + APIKey)
    for cat in catJSON:
        results += "catID: " + str(cat.get('id')) + ": catName: " + cat.get('hint')+ "\n"
    return results   
     
@make_pretty                          
async def getDisplayName(DiscordID):
    nameJSON = await getAccountData(DiscordID)
    result = "Your account name is: " + nameJSON.get('name')
    return result

@make_pretty
async def getRemainingAP(DiscordID):
    accountJSON = await getAccountData(DiscordID)
    result = 15000 - (int(accountJSON.get('daily_ap')) + int(accountJSON.get('monthly_ap')))
    if(result < 15000):
        text = "You have " + str(result) + " remaining. Only " + str(result/10) + " more days before the nightmare ends!"
    else:
        text = "YOU ARE FREE FROM THE NIGHTMARE"
    return text

@make_pretty
async def getGWWikiHTML(query):
    result = getSoup("https://wiki.guildwars2.com/wiki/" + query.replace(" ","_"))
    if result == None:
        return "an error occurred getting your query, boss: " + query
    return result.select("p")[0].getText() + "\n" + result.select("p")[1].getText()

@make_pretty
async def gw2Exchange(currencyType, quantity):
    return await getJSON(gw2_api_url + 'commerce/exchange/'+ currencyType + '?quantity='+ quantity)

#loadItems()
#getItemInfoByName("Jalis")


import WebUtils
import DataBaseUtils
import asyncio

"""
This script creates all tables and loads all items, continents, and currencies to the SQLite database.
"""


async def loadItems(itemsPerChunk):
    itemJSON = await WebUtils.getJSON(WebUtils.gw2_api_url + "items")
    counter = 0
    itemIDs = []
    for item in itemJSON:
        key = str(item)
        if DataBaseUtils.hasItem(key):
            #print(key + " already exists!")
            continue
        else:
            itemIDs.append(key)
            counter += 1
            if counter >= itemsPerChunk:
                itemList = await WebUtils.getJSON(WebUtils.gw2_api_url + "items?ids=" + ",".join(itemIDs))
                itemCounter = 0
                for item in itemList:
                    print(itemIDs[itemCounter])
                    DataBaseUtils.insertQuery(
                        "items", itemIDs[itemCounter], item.get('name'))
                    itemCounter += 1
                counter = 0
                itemIDs = []


async def getGW2ApiData(name):
    url = WebUtils.gw2_api_url + name + "?ids=all"
    itemJSON = await WebUtils.getJSON(url)
    for item in itemJSON:
        key = str(item.get('id'))
        DataBaseUtils.insertQuery(name, key, item.get('name'))
    print("Loaded the " + name + " table!")


async def main():
    DataBaseUtils.createTables()
    await getGW2ApiData("continents")
    await getGW2ApiData("currencies")
    await loadItems(30)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

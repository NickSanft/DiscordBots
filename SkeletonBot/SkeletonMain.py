import discord
import sys
import random
import aiohttp
import time
import datetime
import json
from igdb_api_python.igdb import igdb
from discord.ext import commands
from discord.ext.commands import Bot

"""
This is the main script for the Skeleton Bot for a discord server.

This is a bot primarily used for testing new functionality for other bots,
or simply just memes.
"""
bot = Bot(command_prefix=commands.when_mentioned_or('!skeleton '))
igdb_api_key = ''

# TODO See if the list of the commands can be extracted using discord.py...
BotCommands = {
    'cat': 'gives you a random cat picture from the internet.',
    'commands': 'Displays a list of commands. You are in this one, dude.',
    'emote': 'takes a message and replaces each character with the emoji equivalent.',
    'games': 'find out the games releasing in the next week.',
    'say': 'the bot repeats whatever you say'
}


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    #await bot.send_message(discord.Object(id='311702454762995714'), 'I am awake, daddy!')


@bot.event
async def on_read():
    print("bot logged in")


@bot.command(pass_context=True)
async def say(ctx, *, message):
    await bot.send_message(ctx.message.channel, message)

@bot.command(pass_context=True)
async def emote(ctx, *, message):
    results = ""
    for char in message:
        if char.isalpha():
            results += ":regional_indicator_" + char.lower() + ":"
        else:
            results += char
    await bot.send_message(ctx.message.channel, results)

@bot.command(pass_context=True)
async def games(ctx):
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
    await bot.send_message(ctx.message.channel, resultString)


@bot.command(pass_context=True)
async def commands(ctx):
    await bot.send_message(ctx.message.channel, getCommands())


@bot.command(pass_context=True)
async def cat(ctx):
    async with aiohttp.get('https://aws.random.cat/meow') as r:
        if r.status == 200:
            js = await r.json()
            await bot.send_message(ctx.message.channel, js['file'])
        else:
            await bot.send_message(ctx.message.channel, "Could not get the file: " + str(js['file']))


def getCommands():
    result = "```"
    for command, description in BotCommands.items():
        result += command + ": " + description + "\n"
    result += "```"
    return result

def secondsToDate(ms):
    return datetime.datetime.fromtimestamp(ms).strftime('%Y-%m-%d')

"""
Init script
"""

if len(sys.argv) >= 2:
    bot_token = sys.argv[1]
    igdb_api_key = sys.argv[2]
    bot.run(sys.argv[1])
else:
    print("A bot token was not provided, the script will now end!!!")

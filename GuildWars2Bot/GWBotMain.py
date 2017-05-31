import discord, sys, WebUtils, inspect, random, DataBaseUtils
from discord.ext import commands
from discord.ext.commands import Bot

"""
This is the main script for the Guild Wars 2 Bot for a discord server.

In order to run this script, simply call this from the command line
with the first argument being your Bot Token from the Discord API.
"""

help_attrs = dict(hidden=True)
bot = Bot(command_prefix=commands.when_mentioned_or('!gw2 '),help_attrs=help_attrs)

emotes = ["(／≧ω＼)","(´～｀ヾ)","(๑ÒωÓ๑)","ﾍ(=^･ω･^= )ﾉ","(^･ω･^=)~"]

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.send_message(discord.Object(id='311702454762995714'), 'Guild Wars 2 bot is online!')
    
@bot.event
async def on_read():
    print("bot logged in")

@bot.command(pass_context=True)
async def wiki(ctx, *, message):
    await bot.send_message(ctx.message.channel, await WebUtils.getGWWikiHTML(message))

@bot.group(pass_context=True)
async def continents(ctx):
    await fetchGW2Data(ctx, inspect.getframeinfo(inspect.currentframe()).function)

@bot.group(pass_context=True)
async def characters(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await bot.send_message(ctx.message.channel, await WebUtils.getCharacters(DiscordID))
    else:
        await bot.send_message(ctx.message.channel, "API Key Not Registered!")

@bot.group(pass_context=True)
async def skins(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await bot.send_message(ctx.message.channel, await WebUtils.getSkins(DiscordID))
    else:
        await bot.send_message(ctx.message.channel, "API Key Not Registered!")

@bot.group(pass_context=True)
async def currencies(ctx):
    await fetchGW2Data(ctx, inspect.getframeinfo(inspect.currentframe()).function)

@bot.group(pass_context=True)
async def item(ctx, *, message):
    await bot.send_message(ctx.message.channel, await WebUtils.getItemInfoByName(message))    

@bot.group(pass_context=True)
async def price(ctx, *, message):
    await bot.send_message(ctx.message.channel, await WebUtils.getItemPrice(message))    

@bot.group(pass_context=True)
async def register(ctx, *, message):
    DataBaseUtils.registerAPIKey(ctx.message.author.id,ctx.message.author.display_name, message)
    await bot.send_message(ctx.message.channel, "API Key Registered!")   

@bot.group(pass_context=True)
async def name(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await bot.send_message(ctx.message.channel, await WebUtils.getDisplayName(DiscordID))
    else:
        await bot.send_message(ctx.message.channel, "API Key Not Registered!")

@bot.group(pass_context=True)
async def bank(ctx, *, message):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await bot.send_message(ctx.message.channel, await WebUtils.getBankCount(DiscordID, message))
    else:
        await bot.send_message(ctx.message.channel, "API Key Not Registered!")

@bot.group(pass_context=True)
async def inventory(ctx, *, message):
    DiscordID = ctx.message.author.id
    await bot.send_message(ctx.message.channel, "Please hold on, I need to go through a lot of characters... " + random.choice(emotes))
    if DataBaseUtils.hasAPIKey(DiscordID):
        await bot.send_message(ctx.message.channel, await WebUtils.getCharacterInventory(DiscordID, message))
    else:
        await bot.send_message(ctx.message.channel, "API Key Not Registered!")

@bot.group(pass_context=True)
async def hp(ctx, *, message):
    DiscordID = ctx.message.author.id
    if message == "all":
        message = None
    if DataBaseUtils.hasAPIKey(DiscordID):
        await bot.send_message(ctx.message.channel, await WebUtils.getHeroPoints(DiscordID, message))
    else:
        await bot.send_message(ctx.message.channel, "API Key Not Registered!")        

@bot.group(pass_context=True)
async def materials(ctx, *, message):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await bot.send_message(ctx.message.channel, await WebUtils.getMaterials(DiscordID, message))
    else:
        await bot.send_message(ctx.message.channel, "API Key Not Registered!")
   
    
        
@bot.group(pass_context=True)
async def accountinfo(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await bot.send_message(ctx.message.channel, await WebUtils.getAccountData(DiscordID))
    else:
        await bot.send_message(ctx.message.channel, "API Key Not Registered!")

@bot.group(pass_context=True)
async def world(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await bot.send_message(ctx.message.channel, await WebUtils.getWorld(DiscordID))
    else:
        await bot.send_message(ctx.message.channel, "API Key Not Registered!")
        
@bot.group(pass_context=True)
async def dailyap(ctx):
    DiscordID = ctx.message.author.id
    if DataBaseUtils.hasAPIKey(DiscordID):
        await bot.send_message(ctx.message.channel, await WebUtils.getRemainingAP(DiscordID))
    else:
        await bot.send_message(ctx.message.channel, "API Key Not Registered!")   

@bot.group(pass_context=True)
async def coins(ctx, *, message):
    currencyType = inspect.getframeinfo(inspect.currentframe()).function
    await bot.send_message(ctx.message.channel, await WebUtils.gw2Exchange(currencyType, message))

@bot.group(pass_context=True)
async def gems(ctx, *, message):
    currencyType = inspect.getframeinfo(inspect.currentframe()).function
    await bot.send_message(ctx.message.channel, await WebUtils.gw2Exchange(currencyType, message))

@bot.group(pass_context=True)
async def wallet(ctx, *, message):
    DiscordID = ctx.message.author.id
    if message == "all":
        message = None
    if DataBaseUtils.hasAPIKey(DiscordID):
        await bot.send_message(ctx.message.channel, await WebUtils.getWallet(DiscordID,message))
    else:
        await bot.send_message(ctx.message.channel, "API Key Not Registered!") 

#print(ctx.message.author.id)
#print(ctx.message.author.display_name) 

async def fetchGW2Data(ctx, functionName):
    if DataBaseUtils.countQuery(functionName) == 0:
        await bot.send_message(ctx.message.channel, "Please hold on, this is my first time " + random.choice(emotes))
        await WebUtils.getGW2ApiData(functionName)
    await bot.send_message(ctx.message.channel, DataBaseUtils.selectAllQuery(functionName))  

if len(sys.argv) >= 2:
    bot_token = sys.argv[1]
    bot.run(sys.argv[1])
else:
    print("A bot token was not provided, the script will now end!!!")

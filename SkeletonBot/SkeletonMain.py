import discord, sys, WebUtils, inspect, random, DataBaseUtils
from discord.ext import commands
from discord.ext.commands import Bot

"""
This is the main script for the Skeleton Bot for a discord server.
"""
bot = Bot(command_prefix=commands.when_mentioned_or('!skeleton '))

#TODO See if the list of the commands can be extracted using discord.py...
BotCommands = {
    'commands': 'Displays a list of commands. You are in this one, dude.',
    'gw2api': 'the bot looks up something using the Guild Wars 2 API.',
    'gw2wiki': 'the bot looks up your text on the Guild Wars 2 wiki.',
    'say': 'the bot repeats whatever you say'
    }

emotes = ["(／≧ω＼)","(´～｀ヾ)","(๑ÒωÓ๑)"]

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.send_message(discord.Object(id='311702454762995714'), 'I am awake, daddy!')
    
@bot.event
async def on_read():
    print("bot logged in")


@bot.command(pass_context=True)
async def say(ctx, *, message):
    await bot.send_message(ctx.message.channel, message)

@bot.command(pass_context=True)
async def gw2wiki(ctx, *, message):
    await bot.send_message(ctx.message.channel, WebUtils.getGWWikiHTML(message))

@bot.group(pass_context=True)
async def gw2api(ctx):
    if ctx.invoked_subcommand is None:
        await bot.send_message(ctx.message.channel, "invalid command, boss...")

@gw2api.command(pass_context=True)
async def continents(ctx):
    await fetchGW2Data(ctx, inspect.getframeinfo(inspect.currentframe()).function)

@gw2api.command(pass_context=True)
async def currencies(ctx):
    await fetchGW2Data(ctx, inspect.getframeinfo(inspect.currentframe()).function)

@gw2api.command(pass_context=True)
async def items(ctx):
    await fetchGW2Data(ctx, inspect.getframeinfo(inspect.currentframe()).function)    

@gw2api.command(pass_context=True)
async def register(ctx, *, message):
    DataBaseUtils.registerAPIKey(ctx.message.author.id,ctx.message.author.display_name, message)
    await bot.send_message(ctx.message.channel, "API Key Registered!")   

@gw2api.command(pass_context=True)
async def name(ctx):
    await bot.send_message(ctx.message.channel, str(WebUtils.getDisplayName(ctx.message.author.id)))   

#print(ctx.message.author.id)
#print(ctx.message.author.display_name) 

@bot.command(pass_context=True)
async def commands(ctx):
    await bot.send_message(ctx.message.channel, getCommands())

async def fetchGW2Data(ctx, functionName):
    if DataBaseUtils.countQuery(functionName) == 0:
        await bot.send_message(ctx.message.channel, "Please hold on, this is my first time " + random.choice(emotes))
        WebUtils.getGW2ApiData(functionName)
    await bot.send_message(ctx.message.channel, DataBaseUtils.selectAllQuery(functionName))  

def getCommands():
    result = ""
    for command, description in BotCommands.items():
        result += command + ": " + description + "\n"
    return result

bot.run(sys.argv[1])



import discord, sys, requests, bs4
from discord.ext import commands

from discord.ext.commands import Bot
client = Bot(command_prefix=commands.when_mentioned_or('!skeleton '))

BotCommands = {
    'commands': 'Displays a list of commands. You are in this one, dude.',
    'gw2': 'the bot looks up your text on the Guild Wars 2 wiki.',
    'say': 'the bot repeats whatever you say'
    }

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.send_message(discord.Object(id='311702454762995714'), 'I am awake, daddy!')
    
@client.event
async def on_read():
    print("Client logged in")

"""
@client.command()
async def help(message):
    await client.say(getCommands())    
    """
@client.command(pass_context=True)
async def say(ctx, *, message):
    await client.send_message(ctx.message.channel, message)

@client.command(pass_context=True)
async def gw2(ctx, *, message):
    await client.send_message(ctx.message.channel, getGWSoup(message))

@client.command(pass_context=True)
async def commands(ctx):
    await client.send_message(ctx.message.channel, getCommands())    


def getCommands():
    result = ""
    for command, description in BotCommands.items():
        result += command + ": " + description + "\n"
    return result

def getSoup(url):
    try:
        print('Downloading page %s...' % url)
        res = requests.get(url,headers={'User-Agent': 'Mozilla/5.0'})
        res.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return None
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    return soup

def getGWSoup(query):
    
    result = getSoup("https://wiki.guildwars2.com/wiki/" + query.replace(" ","_"))
    if result == None:
        return "an error occurred getting your query, boss: " + query
    return result.select("p")[0].getText() + "\n" + result.select("p")[1].getText()
    
client.run(sys.argv[1])



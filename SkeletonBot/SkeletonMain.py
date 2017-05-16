import discord, sys, requests, bs4

from discord.ext.commands import Bot
client = Bot(command_prefix="!skeleton")

BotCommands = {
    'help': 'Displays a list of commands. You are in this one, dude.',
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
    
@client.command()
async def hello(*args):
    return await client.say("Hello, friends.")

@client.event
async def on_message(message):
    if message.content.startswith(client.command_prefix):
        if(len(message.content) > len(client.command_prefix)):
            text = message.content[len(client.command_prefix):].strip()
            if(text.startswith('say')):
                print("got here!")
                await client.send_message(message.channel, text[3:])
            elif(text.startswith('gw2')):
                search = text[3:].strip()
                await client.send_message(message.channel, getGWSoup(search))
            elif(text.startswith('help')):
                await client.send_message(message.channel, getCommands())                 
            else:
                print("got there!")
                await client.send_message(message.channel, "Did not recognize command: " + text)


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
    result = getSoup("https://wiki.guildwars2.com/wiki/" + query)
    if result == None:
        return "an error occurred getting your query, boss: " + query
    return result.select("p")[0].getText()
    
client.run(sys.argv[1])



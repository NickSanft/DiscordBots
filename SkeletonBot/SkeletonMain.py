import sys
from discord.ext import commands
from discord.ext.commands import Bot
import IgdbUtils
import CatUtils
import GoogleCalendarUtils

"""
This is the main script for the Skeleton Bot for a discord server.

This is a bot primarily used for testing new functionality for other bots,
or simply just memes.
"""
bot = Bot(command_prefix=commands.when_mentioned_or('!skeleton '))

# TODO See if the list of the commands can be extracted using discord.py...
BotCommands = {
    'cat': 'gives you a random cat picture from the internet.',
    'commands': 'Displays a list of commands. You are in this one, dude.',
    'emote': 'takes a message and replaces each character with the emoji equivalent.',
    'say': 'the bot repeats whatever you say'
}

igdb_api_key = ''


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


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
    await bot.send_message(ctx.message.channel, await IgdbUtils.getGames())


@bot.command(pass_context=True)
async def commandlist(ctx):
    await bot.send_message(ctx.message.channel, getCommands())


@bot.command(pass_context=True)
async def cat(ctx): 
    await bot.send_message(ctx.message.channel, await CatUtils.getCatPicture())

@bot.command(pass_context=True)
async def calendar(ctx, *, message): 
    await bot.send_message(ctx.message.channel, await GoogleCalendarUtils.getCalendarEvents(message))


def getCommands():
    result = "```"
    for command, description in BotCommands.items():
        result += command + ": " + description + "\n"
    result += "```"
    return result

"""
Init script
"""

if len(sys.argv) >= 2:
    bot_token = sys.argv[1]
    igdb_api_key = sys.argv[2]
    bot.run(sys.argv[1])
else:
    print("A bot token was not provided, the script will now end!!!")
import discord
import sys
import random
import aiohttp
from discord.ext import commands
from discord.ext.commands import Bot

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
async def emote(ctx, *, message):
    results = ""
    for char in message:
        if char.isalpha():
            results += ":regional_indicator_" + char.lower() + ":"
        else:
            results += char
    await bot.send_message(ctx.message.channel, results)


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
    result = ""
    for command, description in BotCommands.items():
        result += command + ": " + description + "\n"
    return result


"""
Init script
"""
if len(sys.argv) >= 2:
    bot_token = sys.argv[1]
    bot.run(sys.argv[1])
else:
    print("A bot token was not provided, the script will now end!!!")

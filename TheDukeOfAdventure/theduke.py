import discord, asyncio, sys, time
from discord.ext import commands

import gamedb

#bot.get_channel('312676555514183681')

bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    print(message.author.id, message.channel)

    await bot.process_commands(message)

@bot.command(pass_context=True)
async def join(ctx, name: str = None):

    if name == None:
        await bot.say("What courage; what ENTHUSIASM! You wish to join " +
                      "the game! ...And yet, you have not given me a name " +
                      "by which to call you!\n\n" +
                      "`Usage: $join <name>`")
    else:
        player_id = ctx.message.author.id
        wasAdded = gamedb.add_character(player_id, name)

        if wasAdded:
            await bot.send_message(ctx.message.author, "what up")
            await bot.say(("Welcome, {0}! I've PMed you with information "
                          "about the game and your character!").format(name))
        else:
            await bot.say("You're already playing the game!")

@bot.command(pass_context=True)
async def name(ctx, name: str = None):

    if name == None:
        await bot.say(("If you'd like to change your name, you'll need "
                       "to fill out everything correctly! :kissing_heart:\n\n"
                       "`Usage: $name <new_name>`"))
    else:
        wasUpdated = gamedb.update_name(ctx.message.author.id, name)

        if wasUpdated:
            await bot.say(("From this point forth, you shall be known "
                           "as {0}! Go now, on to adventure! "
                           "TO GLORY!").format(name))
        else:
            print("Oh god something went wrong")



bot.run(sys.argv[1])

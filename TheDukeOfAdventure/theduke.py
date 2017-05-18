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

@bot.command(pass_context=True)
async def summary(ctx):
    result = gamedb.get_character(ctx.message.author.id)

    if result == None:
        await bot.say(("You're not even playing the game! "
                       "Are you too cowardly? Too *weak*? "
                       "Summarize yourself; there is no room for weaklings here!"))
    else:
        print(result)
        msg = ("Here's a summary of your character:\n"
              "```Name: {1}\nLevel {2}\nHealth: {4}/{5}\nFight: {6}\n"
              "Body: {7}\nSpirit: {8}")
        if result[3] > 0:
            msg += "\n\nYou still have {3} unassigned ability points!```"
        else:
            msg += "```"

        await bot.say(msg.format(*result))


bot.run(sys.argv[1])

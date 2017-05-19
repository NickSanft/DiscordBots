import discord, asyncio, sys, time
from discord.ext import commands

import gamedb, strings

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
        await bot.say(strings.all["join"]["notfound"])
    else:
        player_id = ctx.message.author.id
        wasAdded = gamedb.add_character(player_id, name)

        if wasAdded:
            await bot.send_message(ctx.message.author, "what up")
            await bot.say(strings.all["join"]["added"].format(name))
        else:
            await bot.say(strings.all["join"]["exists"])

@bot.command(pass_context=True)
async def name(ctx, name: str = None):

    if name == None:
        await bot.say(strings.all["name"]["notfound"])
    else:
        wasUpdated = gamedb.update_name(ctx.message.author.id, name)

        if wasUpdated:
            await bot.say(strings.all["name"]["updated"].format(name))
        else:
            print(strings.all["name"]["failed"])

@bot.command(pass_context=True)
async def summary(ctx):
    result = gamedb.get_character(ctx.message.author.id)

    # Did not have a character matching id.
    if result == None:
        await bot.say(strings.all["summary"]["notfound"])
    else:
        msg = (strings.all["summary"]["stats"])

        # Include a message stating that there are unspent ability points (or not).
        if result[3] > 0:
            msg += strings.all["summary"]["unspent"]

        await bot.say(msg.format(*result))


bot.run(sys.argv[1])

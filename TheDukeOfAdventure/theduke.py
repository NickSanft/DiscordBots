import discord, asyncio, sys
from discord.ext import commands

import gamedb

#bot.get_channel('312676555514183681')

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'))

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
async def join(ctx):
    player_id = ctx.message.author.id
    gamedb.add_character(player_id)

@bot.command()
async def sql_ver():
    pass

@bot.command(pass_context=True)
async def sql3(ctx, *message: str):
    if ctx.message.author.id == '176131629847281665':
        cur = con.cursor()
        cur.execute(' '.join(message))

        data = cur.fetchall()

        await bot.say(data)

bot.run(sys.argv[1])

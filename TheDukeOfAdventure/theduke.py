import discord, asyncio, sys
from discord.ext import commands
import sqlite3 as sql

#bot.get_channel('312676555514183681')

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'))

con = sql.connect('game.db')

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
    player_nickname = ctx.message.author.display_name

    cur = con.cursor()

    cur.execute("SELECT * FROM Players WHERE user_id=?", (player_id,))
    data = cur.fetchone()
    if data != None:
        await bot.say("You've already joined the game, " + player_nickname + "!")
    else:
        cur.execute("INSERT OR REPLACE INTO Players VALUES (?, ?)", (player_id, player_nickname))

        data = cur.fetchall()
        await bot.say("You're now playing in the Great Test RPG!")


@bot.command()
async def sql_ver():
    cur = con.cursor()
    cur.execute('SELECT SQLITE_VERSION()')

    data = cur.fetchone()

    await bot.say(data)

@bot.command(pass_context=True)
async def sql3(ctx, *message: str):
    if ctx.message.author.id == '176131629847281665':
        cur = con.cursor()
        cur.execute(' '.join(message))

        data = cur.fetchall()

        await bot.say(data)

bot.run(sys.argv[1])

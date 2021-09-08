import discord
import sqlite3
#python3 -m poetry install
import os
from keep_alive import keep_alive


def create_table():
  conn = sqlite3.connect('./data/test.db')
  c = conn.cursor()
  conn.execute('''
  CREATE TABLE IF NOT EXISTS main
  (guild_id int, prefix TEXT, PRIMARY KEY (guild_id))''')
create_table()


import math 
'''
important upadate found a slash commands framework so mabey continue bot??
'''

from discord.ext import commands


intents = discord.Intents.default()
intents.members = True
intents.members = True

def get_prefix(bot, message):
    db = sqlite3.connect("./data/test.db")
    cur = db.cursor()
    cur.execute("SELECT prefix FROM main WHERE guild_id = ?", (message.guild.id,))
    prefix = cur.fetchone()
    if prefix is None:
        prefix = "$" #return default prefix if guild not saved in database.
    else:
        prefix = prefix[0]
    db.close()
    return prefix


bot = commands.Bot( command_prefix=get_prefix, intents =intents )

bot.multiplier = 1
@bot.command()
async def new(ctx, new_pr):
    if ctx.message.author.guild_permissions.manage_messages:
        db = sqlite3.connect('./data/test.db')
        cursor = db.cursor()
        cursor.execute(f"SELECT prefix FROM main WHERE guild_id = {ctx.guild.id}")
        prefix = cursor.fetchone()
        if prefix is None:
            sql = ("INSERT INTO main(guild_id, prefix) VALUES(?,?)")
            val = (ctx.guild.id, new_pr)
            prefixsetem = discord.Embed(title=f"<:Success:835190431758549043> **{ctx.guild.name}**'s prefix set to `{new_pr}`", description=f"Set by **{ctx.author}**", color=0x03fc45)
            await ctx.send(embed=prefixsetem)
        elif prefix is not None:
            sql = ("UPDATE main SET prefix = ? WHERE guild_id = ?")
            val = (new_pr, ctx.guild.id)
            prefixsetem = discord.Embed(title=f"<:Success:835190431758549043> **{ctx.guild.name}**'s prefix updated to `{new_pr}`", description=f"Updated by **{ctx.author}**", color=0x03fc45)
            await ctx.send(embed=prefixsetem)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

bot.warnings = {} # guild_id : {member_id: [count, [(admin_id, reason)]]}


    





@bot.event
async def on_ready():
  
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
@commands.has_permissions(administrator =True)
async def load(ctx, extension):
  bot.load_extension(f'cogs.{extension}')


@bot.command()
@commands.has_permissions(administrator =True)
async def unload(ctx, extension):
  bot.unload_extension(f'cogs.{extension}')

@bot.command()
@commands.has_permissions(administrator =True)
async def reload(ctx, extension):
  bot.unload_extension(f'cogs.{extension}')
  bot.load_extension(f'cogs.{extension}')
  await ctx.channel.send('reloaded')



keep_alive()


bot.run(os.environ('TOKEN'))



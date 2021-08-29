'''
Final Update

'''



import discord
#python3 -m poetry install
import os
from keep_alive import keep_alive
import aiosqlite
import asyncio

import math 

from discord.ext import commands


intents = discord.Intents.default()
intents.members = True
intents.members = True


bot = commands.Bot(    command_prefix=['!', '$']
, intents =intents )

bot.multiplier = 1



bot.warnings = {} # guild_id : {member_id: [count, [(admin_id, reason)]]}

async def initialize():
    await bot.wait_until_ready()
    bot.db = await aiosqlite.connect("./data/database.db")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS guildData (guild_id int, user_id int, exp int, warn_reason TEXT, PRIMARY KEY (guild_id, user_id))")
    await bot.db.execute("CREATE TABLE IF NOT EXISTS testTable (guild_id int, name text, PRIMARY KEY (guild_id))")

#    await bot.db.execute("CREATE TABLE IF NOT EXISTS Channels (guild_id text, logs_channel text PRIMARY KEY (guild_id) ) ")




    





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

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')


keep_alive()

bot.loop.create_task(initialize())
bot.run(os.getenv('TOKEN'))
asyncio.run(bot.db.close())


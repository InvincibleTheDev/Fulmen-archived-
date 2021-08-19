import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
intents = discord.Intents().all()
intents.members = True

bot = commands.Bot(command_prefix='$', intents =intents )


@bot.event
async def on_member_join(member): 
    rank = discord.utils.get(member.guild.roles, name="member") #Bot get guild(server) roles
    await member.add_roles(rank)
    print(f"{member} was given the {rank} role.")
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


@bot.command()
@commands.has_permissions(administrator =True)
async def config(ctx, message):
  async with ctx.typing():
    await ctx.send(f'success fully configged {message}')

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')


keep_alive()
bot.run(os.getenv('TOKEN'))

import discord 
from discord.ext import commands
from main import initialize

class Config(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  initialize()
  
  @commands.command()
  async def save_name(self, ctx, name):
    self.bot.db.execute("""
    INSERT INTO testTable
     (guild_id, name) 
     VALUES (?,?)
    """, (ctx.guild.id, name) )
  @commands.command()
  async def tell_name(self, ctx):
    cur = await self.bot.db.execute("SELECT name FROM testTable WHERE   guild_id = ?", (ctx.guild.id)  )
    data = cur.fetchnote()
    name = data[0]
    await ctx.send(name)
    

  







def setup(bot):
	bot.add_cog(Config(bot))
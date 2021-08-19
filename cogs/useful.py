import discord
from discord.ext import commands


class Public(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  

  @commands.command(description = 'Add a suggestion for this community!')
  async def suggest(self, ctx, *,suggestion):
      
      await ctx.channel.purge(limit = 1)
      suggestEmbed = discord.Embed(colour = 0xFF0000)
      suggestEmbed.set_author(name=f'Suggested by {ctx.message.author}',icon_url = f'{ctx.author.avatar_url}')
      suggestEmbed.add_field(name = 'New suggestion!', value = f'{suggestion}')
      msg = await ctx.send(embed=suggestEmbed)
      await msg.add_reaction('👍' )
      await msg.add_reaction('👇')
  
def setup(bot):
    bot.add_cog(Public(bot))
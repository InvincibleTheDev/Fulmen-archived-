import discord 
from discord.ext import commands

class Logs(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.Cog.listener()
  async def on_guild_channel_delete(self,channel):
    log_channel = discord.utils.get (self.bot.get_all_channels(), name="staff-logs")

    entry = await channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete, limit=1).get()

    embed=discord.Embed(title="!!CHANNEL WAS DELETED!!", description="Another channel was deleted", color=0xff2600)
    embed.add_field(name="Who Deleted The Channel", value=entry.user.name, inline=False)
    embed.add_field(name="The Channel That Was Deleted", value=channel.name, inline=False)
    embed.add_field(name="When It Was Deleted", value=entry.created_at, inline=True)


    await log_channel.send(embed=embed)
  @commands.Cog.listener()
  async def on_guild_channel_create(self, channel):
    log_channel = discord.utils.get (self.bot.get_all_channels(), name="staff-logs")

    entry = await channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete, limit=1).get()
    print('hello world')
    embed=discord.Embed(title="!!CHANNEL WAS Created!!", description="Another channel was Created", color=0xff2600)
    embed.add_field(name="Who Created The Channel", value=entry.user.name, inline=False)
    embed.add_field(name="The Channel That Was Created", value=channel.name, inline=False)
    embed.add_field(name="When It Was Created", value=entry.created_at, inline=True)
    await log_channel.send(embed=embed)






def setup(bot):
  bot.add_cog(Logs(bot))
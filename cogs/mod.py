import discord
from discord.ext import commands

class Moderation(commands.Cog):
  def __init__(self, bot):
   self.bot = bot


  @commands.command()
  async def avatar(self, ctx, member: discord.Member):
    userAvatarUrl = member.avatar_url
    await ctx.send(userAvatarUrl)
  @commands.command()
  @commands.has_permissions(manage_messages =True)
  async def clear(self, ctx, amount=10):
        await ctx.channel.purge(limit=amount)
        
        await ctx.channel.send(f'{amount} Messages Deleted', delete_after=10.0)

 

  @commands.command(description="kick a member")
  @commands.has_permissions(kick_members = True)
  async def kick(self,ctx, member : discord.Member ,*, reason=None):
    log_channel = discord.utils.get(ctx.guild.channels, name="staff-logs")

    if reason == None:
      await ctx.send('please provide a reason')
    else:
      await member.kick(reason = reason)
      auth = ctx.message.author.name

      await ctx.send(f'{member} has been kicked for {reason}')
    

      embed=discord.Embed(title="!!SOME WAS KICKED!!", description="Server log there was A KICK", color=0xff0000)

      embed.add_field(name="Person Who Was Muted", value=f"{member}", inline=False)
      embed.add_field(name="Person Who Muted By", value=f"{auth}", inline=False)
      embed.add_field(name="Reason Was", value=f"{reason}", inline=False)


      await log_channel.send(embed=embed)
    




 
 
  @commands.command(description='ban a member')
  @commands.has_permissions(ban_members = True)
  async def ban(self,ctx, member : discord.Member ,*, reason=None):
    log_channel = discord.utils.get(ctx.guild.channels, name="staff-logs")

    if reason == None:
      await ctx.send('please provide a reason')
    else:
      await member.ban(reason = reason)
      auth = ctx.message.author.name

      await ctx.send(f'{member} has been Banned for {reason}')
    

      embed=discord.Embed(title="!!SOME WAS BANNED!!", description="Server log there was A KICK", color=0xff0000)

      embed.add_field(name="Person Who Was BANNED", value=f"{member}", inline=False)
      embed.add_field(name="Person Who BANNED By", value=f"{auth}", inline=False)
      embed.add_field(name="Reason Was", value=f"{reason}", inline=False)


      await log_channel.send(embed=embed)

  @commands.command(description='unban a member')
  @commands.has_permissions(ban_members = True)
  async def unban(self, ctx, *, member):
    banned_users = await ctx.guild.bans()
     
    member_name, member_discriminator = member.split('#')
    for ban_entry in banned_users:
    	user = ban_entry.user

    	if (user.name, user.discriminator) == (member_name, member_discriminator):
    		await ctx.guild.unban(user)
    		await ctx.channel.send(f"Unbanned: {user.mention}")
  
  
  
 
  
def setup(bot):
  bot.add_cog(Moderation(bot))
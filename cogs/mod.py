import discord
from discord.ext import commands
import aiofiles
from datetime import datetime
from typing import Optional

from discord import Embed, Member
from discord.ext.commands import Cog

from io import BytesIO

import aiohttp
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
  @commands.command()
  @commands.has_permissions(manage_messages =True)
  async def createemoji(self,ctx, url: str, *, name):
  	guild = ctx.guild
  	if ctx.author.guild_permissions.manage_emojis:
  		async with aiohttp.ClientSession() as ses:
  			async with ses.get(url) as r:
        
  				try:
  					img_or_gif = BytesIO(await r.read())
  					b_value = img_or_gif.getvalue()
  					if r.status in range(200, 299):
  						emoji = await guild.create_custom_emoji (image=b_value, name=name)
  						await ctx.send(f'Successfully created   emoji: <:{name}:{emoji.id}>')
  						await ses.close()
  					else:
  						await ctx.send(f'Error when making  request | {r.status} response.')
  						await ses.close()
  
  				except discord.HTTPException:
  					await ctx.send('File size is too big!')

  @commands.command()
  @commands.has_permissions(manage_messages =True)
  async def deleteemoji(self, ctx, emoji: discord.Emoji):
  	guild = ctx.guild
  	if ctx.author.guild_permissions.manage_emojis:
  		await ctx.send(f'Successfully deleted (or not):   {emoji}')
  		await emoji.delete()
  
  

 

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
  @commands.Cog.listener()
  async def on_ready(self):
      for guild in self.bot.guilds:
          self.bot.warnings[guild.id] = {}
        
          async with aiofiles.open(f"./data/{guild.id}.txt", mode="a") as temp:
              pass

          async with aiofiles.open(f"./data/{guild.id}.txt", mode="r") as file:
            lines = await file.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                reason = " ".join(data[2:]).strip("\n")

                try:
                    self.bot.warnings[guild.id][member_id][0] += 1
                    self.bot.warnings[guild.id][member_id][1].append((admin_id, reason))

                except KeyError:
                    self.bot.warnings[guild.id][member_id] = [1, [(admin_id, reason)]] 
    
      print(self.bot.user.name + " is ready.")

  @commands.Cog.listener()
  async def on_guild_join(self,guild):
      self.bot.warnings[guild.id] = {}

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def warn(self,ctx, member: discord.Member=None, *, reason=None):
      if member is None:
          return await ctx.send("The provided member could not be found or you forgot to provide one.")
        
      if reason is None:
          return await ctx.send("Please provide a reason for warning this user.")

      try:
          first_warning = False
          self.bot.warnings[ctx.guild.id][member.id][0] += 1
          self.bot.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))

      except KeyError:
          first_warning = True
          self.bot.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]

      count = self.bot.warnings[ctx.guild.id][member.id][0]

      async with aiofiles.open(f"./data/{ctx.guild.id}.txt", mode="a") as file:
        await file.write(f"{member.id} {ctx.author.id} {reason}\n")

      await ctx.send(f"{member.mention} has {count} {'warning' if first_warning else 'warnings'}.")

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def warnings(self,ctx, member: discord.Member=None):
      if member is None:
          return await ctx.send("The provided member could not be found or you forgot to provide one.")
    
      embed = discord.Embed(title=f"Displaying Warnings for {member.name}", description="", colour=discord.Colour.red())
      try:
          i = 1
          for admin_id, reason in self.bot.warnings[ctx.guild.id][member.id][1]:
              admin = ctx.guild.get_member(admin_id)
              embed.description += f"**Warning {i}** given by: {admin.mention} for: *'{reason}'*.\n"
              i += 1

          await ctx.send(embed=embed)

      except KeyError: # no warnings
          await ctx.send("This user has no warnings.")

  
  
  
 
  
def setup(bot):
  bot.add_cog(Moderation(bot))
import discord 
from discord.ext import commands
import math
import asyncio 
   
from main import initialize

class Level(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  initialize()
  @commands.Cog.listener()
  async def on_message(self,message):




      if not message.author.bot:
          cursor = await self.bot.db.execute("INSERT OR IGNORE INTO guildData  (guild_id, user_id, exp) VALUES (?,?,?)", (message.guild.id,   message.author.id, 1)) 

          if cursor.rowcount == 0:
              await self.bot.db.execute("UPDATE guildData SET exp = exp + 1 WHERE  guild_id = ? AND user_id = ?", (message.guild.id, message.author.id) )
              cur = await self.bot.db.execute("SELECT exp FROM guildData WHERE   guild_id = ? AND user_id = ?", (message.guild.id, message.author.id)  )
              data = await cur.fetchone()
              exp = data[0]
              lvl = math.sqrt(exp) / self.bot.multiplier
              member = message.author
              level_channel = discord.utils.get(message.guild.text_channels, name="level-ups")



              if lvl.is_integer():
                  async with self.bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ?",   (message.guild.id,)) as cursor:
                      rank = 1
                      async for value in cursor:
                        if exp < value[0]:
                         rank += 1

                  '''
                  if int(lvl) == 1:
                    member.add_role(level1_role)
                    await message.channel.send(f"{member.mention} well done!  You're now level: {int(lvl)}. and you now have the   {level1_role}")

                  elif int(lvl) == 5:
                    member.add_role(level10_role) 
                    await message.channel.send(f"{member.mention} well done!  You're now level: {int(lvl)}. and you now have the   {level10_role}")

                  elif int(lvl) == 10:
                    member.add_role(level15_role)
                    await message.channel.send(f"{member.mention} well done!  You're now level: {int(lvl)}. and you now have the   {level15_role}")

                  elif int(lvl) == 15:
                    member.add_role(level15_role)
                  else:
                  '''
                  embed=discord.Embed(title="You Levelled UP", description=f"hey {member.mention} good job you levelled up !!")
                  embed.set_author(name=member.mention, icon_url=member.avatar_url)
                  embed.set_thumbnail(url=member.avatar_url)
                  embed.add_field(name="your level", value=lvl, inline=False)
                  embed.add_field(name="Your Rank", value=rank, inline=True)

                  await level_channel.send(f"{member.mention} well done!",embed=embed )

          await self.bot.db.commit()














  @commands.command(aliases=['stats','level'])
  async def rank(self,ctx, member: discord.Member=None):

      if member is None: member = ctx.author

      # get user exp
      async with self.bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ? AND   user_id = ?", (ctx.guild.id, member.id)) as cursor:
          data = await cursor.fetchone()
          exp = data[0]

          # calculate rank
      async with self.bot.db.execute("SELECT exp FROM guildData WHERE guild_id = ?",   (ctx.guild.id,)) as cursor:
          rank = 1
          async for value in cursor:
              if exp < value[0]:
                  rank += 1

      lvl = int(math.sqrt(exp)// self.bot.multiplier)

      current_lvl_exp = (self.bot.multiplier*(lvl))**2
      next_lvl_exp = (self.bot.multiplier*((lvl+1)))**2

      lvl_percentage = ((exp-current_lvl_exp) / (next_lvl_exp-current_lvl_exp)) *   100

      embed = discord.Embed(title=f"Stats for {member.name}",   colour=discord.Colour.gold())
      embed.add_field(name="Level", value=str(lvl), inline=False)
      embed.add_field(name="Exp", value=f"{exp}/{next_lvl_exp}", inline=False)
      embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}",  inline=False)
      embed.add_field(name="Level Progress", value=f"{round(lvl_percentage, 2)}%",   inline=False)

      await ctx.send(embed=embed)

  @commands.command()
  async def leaderboard(self,ctx): 

      buttons = {}
      for i in range(1, 6):
          buttons[f"{i}\N{COMBINING ENCLOSING KEYCAP}"] = i # only show first 5   pages

      previous_page = 0
      current = 1
      index = 1
      entries_per_page = 10

      embed = discord.Embed(title=f"Leaderboard Page {current}", description="",  colour=discord.Colour.gold())
      msg = await ctx.send(embed=embed)

      for button in buttons:
          await msg.add_reaction(button)

      while True:
          if current != previous_page:
              embed.title = f"Leaderboard Page {current}"
              embed.description = ""

              async with self.bot.db.execute(f"SELECT user_id, exp FROM guildData  WHERE guild_id = ? ORDER BY exp DESC LIMIT ? OFFSET ? ",   (ctx.guild.id, entries_per_page, entries_per_page*(current-1),)) as   cursor:
                  index = entries_per_page*(current-1)

                  async for entry in cursor:
                      index += 1
                      member_id, exp = entry
                      member = ctx.guild.get_member(member_id)
                      embed.description += f"{index}) {member.mention} : {exp}\n"

                  await msg.edit(embed=embed)

          try:
              reaction, user = await self.bot.wait_for("reaction_add", check=lambda  reaction, user: user == ctx.author and reaction.emoji in buttons,  timeout=60.0)

          except asyncio.TimeoutError:
              return await msg.clear_reactions()

          else:
              previous_page = current
              await msg.remove_reaction(reaction.emoji, ctx.author)
              current = buttons[reaction.emoji]


  

  


def setup(bot):
	bot.add_cog(Level(bot))
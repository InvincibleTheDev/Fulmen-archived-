import asyncio
import datetime
import random
import discord

import random

from datetime import date, datetime
from discord import guild
from discord.ext import commands
from discord.utils import get


class MemberEvents(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        guild_id = payload.guild_id
        guild = self.bot.get_guild(guild_id)

        user_id = payload.user_id
        user = self.bot.get_user(user_id)

        channel_id = payload.channel_id
        channel = self.bot.get_channel(channel_id)

        message_id = payload.message_id
        emoji = payload.emoji.name

        ticket_id = random.randint(1,100000000)

        ######################### TICKETS #########################

        if emoji == "📩":

            message = await channel.fetch_message(message_id)
            await message.remove_reaction("📩",user)





            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            support_role = discord.utils.get(guild.roles, name = "Support")
            category = discord.utils.get(guild.categories, name = "Tickets")

            if support_role is None:

                await guild.create_role(name="Support")

            if category is None:

                    new_category = await guild.create_category(name="Tickets")
                    category = guild.get_channel(new_category.id)

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                support_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
            }

            ticket_channel_name = await category.create_text_channel(f'ticket-{random.randint(100,999)}', overwrites=overwrites)
            ticket_channel_id = (f'ticket_channel_name-{random.randint(100,999)}')


            guild.id, str((ticket_channel_name), ticket_channel_id, user_id)

            embed = discord.Embed(title="How can we help you?", color=0xf7fcfd)
            embed.add_field(name="✅ Claim the Ticket!", value="```Claim the ticket so that the other supporters know that it is already being processed.```", inline=False)
            embed.add_field(name="📌 Inform the Support about your Ticket", value="```Inform the other supporters about your ticket to guarantee a quick processing.```", inline=False)
            embed.add_field(name="🔒 Close the Ticket!", value="```Close the ticket as soon as the problem has been resolved.```", inline=False)

            embed.set_author(name="TiLiKas Ticket Bot")
            embed.set_image(url="https://cdn.discordapp.com/attachments/771635939700768769/839483919786704926/iu.png")

            ticket_channel_message = await ticket_channel_name.send(embed=embed)

            await ticket_channel_message.add_reaction("✅")
            await ticket_channel_message.add_reaction("📌")
            await ticket_channel_message.add_reaction("🔒")


        if emoji == "✅" and user.bot == False:









           embed = discord.Embed
           title = "Ticket claimed!",
           description = f"``‼️ The ticket was claimed by {user.mention},"
           color = 0xf7
           await channel.send(embed=embed)
        channel_name = f'{ticket_id}-ticket'
        
        if emoji == "🔒" and user.bot == False:



            embed = discord.Embed(
                title = "Ticket closed!",
                description = f"``🎟️ The ticket was just closed by {user.name}.``",
                color = 0xf7fcfd)

            await channel.send(embed=embed)
            await asyncio.sleep(10)
            await channel.delete()

            channel_log = discord.utils.get(guild.text_channels, name="overall-log")
            overwrites = {guild.default_role: discord.PermissionOverwrite(send_messages=False)}

            if channel_log is None:

                channel_log = await guild.create_text_channel("overall-log", overwrites=overwrites)

            embed = discord.Embed(
                title = "Closed Ticket",
                description = f"The {channel_name} was closed by {user.mention}",
                timestamp = datetime.utcnow(),
                color = 0xf7fcfd)

            await channel_log.send(embed=embed)




def setup(bot):
    bot.add_cog(MemberEvents(bot))
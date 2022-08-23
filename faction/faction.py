import asyncio
import emoji
import re
import typing
import random

import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel

class Faction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.api.get_plugin_partition(self)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not payload.guild_id:
            return

        if payload.message_id != 1011527189000368188:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = discord.utils.get(guild.members, id=payload.user_id)

        if member.bot:
            return

        # Bonanus, Bosacius, Indarias, Menogias
        role_ids = [1011529826605207553, 1011529080316895244, 1011529721441439796, 1011530283264262154]
        
        # Make sure they don't have a role already
        for role_id in role_ids:
            role = discord.utils.get(guild.roles, id=role_id)
            if role in member.roles:
                return

        assigned_role_id = role_ids[random.randrange(4)]
        assigned_role = discord.utils.get(guild.roles, id=assigned_role_id)

        if assigned_role:
            await member.add_roles(assigned_role)

def setup(bot):
    bot.add_cog(Faction(bot))


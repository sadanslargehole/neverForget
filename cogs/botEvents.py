import discord
from discord.ext import commands
from classes.bot import bot
from classes.Models import guild

class botEvents:
    def __init__(self, robot: bot):
        self.bot = robot

    @commands.Cog.listener("guild join")
    async def guildJoin(self, guildJoined: discord.Guild):
        if guild.filter(id=guildJoined.id).exists():


    @commands.Cog.listener("message button click")
    async def onButtonthingieClick(self, ):
        # whitelist/blacklist
        #
        pass

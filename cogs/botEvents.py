import discord
from discord.ext import commands
from classes.bot import bot


class botEvents:
    def __init__(self, robot: bot):
        self.bot = robot

    @commands.Cog.listener("guild join")
    async def guildJoin(self, guild: discord.Guild):
        x = self.bot.getGuildOrNone(guild.id)
        if not x:
            # TODO: create the guild db entry
            self.bot.guild_db.create()

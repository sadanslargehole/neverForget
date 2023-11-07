import discord
from discord.ext import commands

import util
from classes.Models import guild
from util import setupGuild, getOrCreateGuild


class botEvents(commands.Cog):
    def __init__(self, robot: commands.Bot):
        self.bot = robot

    @commands.Cog.listener(name="on_guild_join")
    async def guildJoin(self, guildJoined: discord.Guild):
        guildDB = await getOrCreateGuild(guild.id)
        await setupGuild(self.bot, guildJoined)


async def setup(bot: commands.Bot):
    await bot.add_cog(botEvents(bot))
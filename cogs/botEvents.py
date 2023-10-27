import discord
from discord.ext import commands
from classes.Models import guild


class botEvents(commands.Cog):
    def __init__(self, robot: commands.Bot):
        self.bot = robot

    @commands.Cog.listener("guild join")
    async def guildJoin(self, guildJoined: discord.Guild):
        guildDB = guild.get_or_none(id)


async def setup(bot: commands.Bot):
    await bot.add_cog(botEvents(bot))
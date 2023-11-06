import discord
from discord.ext import commands


class cogName(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["1", "2"])
    async def thisIsACommand(self, ctx: commands.Context, *args):
        # DO SOMETHING
        pass


async def setup(bot: commands.Bot):
    await bot.add_cog(cogName(bot))


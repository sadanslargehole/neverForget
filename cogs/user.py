import discord
from discord.ext import commands


class cogName(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx: commands.Context, *args):
        await ctx.message.reply("made by <@>\ncontact to report bugs\n[source code](https://example.com) is avilable "
                                "on github")


async def setup(bot: commands.Bot):
    await bot.add_cog(cogName(bot))


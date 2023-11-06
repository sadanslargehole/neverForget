import discord
from discord.ext import commands
from classes.bot import bot as BadBot
from discord.ext.commands import BucketType


class cogName(commands.Cog):
    def __init__(self, bot: BadBot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(2, 60, BucketType.user)
    async def info(self, ctx: commands.Context):
        await ctx.message.reply(
            "made by <@521819891141967883>\ncontact to report bugs\n[source code](https://github.com/sadanslargehole/neverForget) is avilable "
            "on github")

    @commands.command()
    @commands.cooldown(2, 60, BucketType.user)
    async def status(self, ctx: commands.Context):
        """ get status of the bot """
        await ctx.reply(str(self.bot.enabled))


async def setup(bot: BadBot):
    await bot.add_cog(cogName(bot))

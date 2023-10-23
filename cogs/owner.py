import discord
from discord.ext import commands


class cogName(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command("quit")
    async def exit(self, ctx: commands.Context, *args):
        print(f"exited by {ctx.author.name} with reason:\n {' '.join(args)}")


async def setup(bot: commands.Bot):
    await bot.add_cog(cogName(bot))


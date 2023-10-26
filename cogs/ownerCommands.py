import discord
from discord.ext import commands


class ownerCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['quit'])
    async def exit(self, ctx: commands.Context, *args):
        print(f"exited by {ctx.author.name} with reason:\n {' '.join(args)}")

    @commands.command(aliases=["dm", "msg"])
    async def message(self, ctx: commands.Context, user: int, *message):
        message = ' '.join(message)
        await self.bot.get_user(user).send(content=message)
        await ctx.message.add_reaction("✔")


    @commands.is_owner()
    @commands.command()
    async def send(self, ctx: commands.Context, channelID: int, *args):
        await self.bot.get_channel(channelID).send(' '.join(args))
        await ctx.message.add_reaction("✔")


async def setup(bot: commands.Bot):
    await bot.add_cog(ownerCommands(bot))


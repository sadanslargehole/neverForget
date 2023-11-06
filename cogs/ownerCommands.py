import discord
from discord.ext import commands

from classes.Models import guild
from util import genDefaultGuild


class ownerCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(aliases=['quit'])
    async def exit(self, ctx: commands.Context, *args):
        print(f"exited by {ctx.author.name} with reason:\n {' '.join(args)}")
        exit(0)

    @commands.is_owner()
    @commands.command(aliases=["dm", "msg"])
    async def message(self, ctx: commands.Context, target: int, *message):
        message = ' '.join(message)
        await self.bot.get_user(target).send(content=message)
        await ctx.message.add_reaction("✔")

    @commands.is_owner()
    @commands.group(invoke_without_command=True)
    async def db(self, ctx: commands.Context, *args):
        await ctx.reply("nope :3")

    @commands.command()
    @commands.is_owner()
    async def send(self, ctx: commands.Context, channelID: int, *args):
        await self.bot.get_channel(channelID).send(' '.join(args))
        await ctx.message.add_reaction("✔")

    @db.command()
    @commands.is_owner()
    async def genGuildDB(self, ctx: commands.Context, guildID: int | None = None):
        if isinstance(ctx.channel, discord.DMChannel) and not guildID:
            raise commands.MissingRequiredArgument(ctx.command.params['guildID'])
        guildID = guildID or ctx.guild.id
        entry = await guild.get_or_none(id=guildID)
        if entry:
            await entry.delete()
        await genDefaultGuild(guildID)
        await ctx.message.add_reaction('✔')


async def setup(bot: commands.Bot):
    await bot.add_cog(ownerCommands(bot))

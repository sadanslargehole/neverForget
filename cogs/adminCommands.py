import discord
from discord.ext import commands
from classes.Models import guild, user

guild_fields = ["canUseBot", "unpinChannel", "enabled", 'whitelist', 'whitelistedChannels', 'blacklistedChannels', 'blacklistedUsers']


class adminCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.group(invoke_without_command=True)
    @commands.command()
    # lifted right from [letters](https://github.com/keli5/LettersBotPY/blob/master/cogs/owner.py) ty :3
    async def log(self, ctx: commands.Context):
        guild_entry = await guild[ctx.guild.id]
        getEmbed = discord.Embed(
            title=f"Guild.{ctx.guild.id}"
        )
        for field in guild_fields:
            attr = ""
            try:
                attr =  getattr(guild_entry, field)
                getEmbed.add_field(name=field, value=attr)
            except AttributeError:
                pass
        await ctx.reply(embed=getEmbed)

    @commands.group('log')
    @commands.command()
    async def setup(self, ctx: commands.Context):
        # TODO: create channel with perms
        pass

    @commands.group('log')
    @commands.command()
    async def set(self, ctx: commands.Context, channelID):
        await guild.filter(id=ctx.guild.id).update(unpinChannel=channelID)
        await ctx.message.add_reaction('✔')


    @commands.has_guild_permissions(manage_guild=True)
    @commands.group(invoke_without_command=True)
    @commands.command()
    async def mode(self, ctx: commands.Context):
        await ctx.reply("[usage](https://github.com/sadanslargehole/neverForget/blob/master/_SETUP/modeUsage.md)")

    async def set(self, ctx:commands.Context, mode:str):
        if mode == "wlist" or "whitelist":
            # TODO:
            pass
        pass


async def setup(bot: commands.Bot):
    await bot.add_cog(adminCommands(bot))


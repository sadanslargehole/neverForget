import discord
from discord import Role, Member, Object, PermissionOverwrite
from discord.ext import commands

import util
from classes.Models import guild, user
from format import formatMessage
from util import getOrCreateGuild
from typing import Union, Dict

guild_fields = ["canUseBot", "unpinChannel", "enabled", 'whitelist', 'whitelistedChannels', 'blacklistedChannels',
                'blacklistedUsers']


class adminCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.has_guild_permissions(manage_guild=True)
    @commands.group(invoke_without_command=True)
    async def wlist(self, ctx: commands.Context):
        await ctx.reply("LINK TO WHITELSIT USAGE")

    @commands.has_guild_permissions(manage_guild=True)
    @commands.command(name="setupMessage")
    async def setupMessage(self, ctx: commands.Context):
        await util.setupGuild(self.bot, ctx.guild, ctx.author, ctx.channel)
        await ctx.message.add_reaction('✔')

    @commands.has_guild_permissions(manage_guild=True)
    @wlist.command(name='add')
    async def wlist_add(self, ctx: commands.Context, channelID):
        guildDB = await getOrCreateGuild(ctx.guild.id)
        guildDB.whitelistedChannels.append(channelID)

    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.group(invoke_without_command=True)
    # lifted right from [letters](https://github.com/keli5/LettersBotPY/blob/master/cogs/owner.py) ty :3
    async def log(self, ctx: commands.Context):
        guild_entry = await getOrCreateGuild(ctx.guild.id)
        getEmbed = discord.Embed(
            title=f"Guild.{ctx.guild.id}"
        )
        for field in guild_fields:
            attr = ""
            try:
                attr = getattr(guild_entry, field)
                getEmbed.add_field(name=field, value=attr)
            except AttributeError:
                pass
        await ctx.reply(embed=getEmbed)

    # TODO: Do this
    @log.command()
    @commands.has_guild_permissions(manage_guild=True)
    async def setup(self, ctx: commands.Context):
        channel = await ctx.guild.create_text_channel('Pinned-Messages-Log')
        # allow roles to send messages
        overites: Dict[Union[Role, Member, Object], PermissionOverwrite] = {
            ctx.guild.default_role: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=False
            )
        }
        for role in ctx.guild.roles:
            if role.permissions.manage_guild or role.permissions.manage_messages or role.permissions.manage_channels:
                overites[role] = discord.PermissionOverwrite(read_messages=True,
                                                             manage_messages=True,
                                                             send_messages=True)
        await channel.edit(overwrites=overites)
        guildDB = await getOrCreateGuild(ctx.guild.id)
        guildDB.unpinChannel = channel.id
        await guildDB.save()
        await ctx.message.add_reaction('✔')

    @log.command(name="msg")
    @commands.has_guild_permissions(manage_guild=True)
    async def log_msg(self, ctx: commands.Context, messageID):
        after = await ctx.channel.fetch_message(messageID)
        guildDB = await getOrCreateGuild(after.guild.id)
        if not guildDB.unpinChannel:
            return
        embed = await formatMessage(after)
        await after.guild.get_channel(guildDB.unpinChannel).send(embed=embed)

    @log.command(name="set")
    @commands.has_guild_permissions(manage_guild=True)
    async def log_set(self, ctx: commands.Context, arg1):
        guildDB = await getOrCreateGuild(ctx.guild.id)
        guildDB.unpinChannel = arg1
        await guildDB.save()
        await ctx.message.add_reaction('✔')

    @commands.has_guild_permissions(manage_guild=True)
    @commands.group(invoke_without_command=True)
    async def mode(self, ctx: commands.Context):
        await ctx.reply("[usage](https://github.com/sadanslargehole/neverForget/blob/master/_SETUP/modeUsage.md)")

    @commands.has_guild_permissions(manage_guild=True)
    @mode.command(name="set")
    async def mode_set(self, ctx: commands.Context, mode: str):
        if not mode:
            raise commands.MissingRequiredArgument(mode)
        if mode.lower() == "wlist" or "whitelist":
            dbguild = await guild[ctx.guild.id]
            dbguild.whitelist = True
            await dbguild.save()
            await ctx.message.add_reaction("✅")
        elif mode.lower() == "blist" or "blacklist":
            dbguild = await guild[ctx.guild.id]
            dbguild.whitelist = False
            await dbguild.save()
            await ctx.message.add_reaction("✅")
        else:
            raise commands.BadArgument(mode)


async def setup(bot: commands.Bot):
    await bot.add_cog(adminCommands(bot))

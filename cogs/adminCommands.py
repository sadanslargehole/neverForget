import discord
from discord import Role, Member, Object, PermissionOverwrite
from discord.ext import commands

import util
from classes.Models import guild, user
from format import formatMessage
from util import getOrCreateGuild
from util import genEnableMessage
from typing import Union, Dict

guild_fields = ["canUseBot", "unpinChannel", "enabled", 'whitelist', 'whitelistedChannels', 'blacklistedChannels',
                'blacklistedUsers']


class adminCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.group(invoke_without_command=True)
    async def wlist(self, ctx: commands.Context):
        await ctx.reply("LINK TO WHITELSIT USAGE")

    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @wlist.command(name='add')
    async def wlist_add(self, ctx: commands.Context, channelID=None):
        channelID = int(channelID or ctx.channel.id)
        guildDB = await getOrCreateGuild(ctx.guild.id)
        if guildDB.whitelistedChannels.__contains__(channelID):
            await ctx.reply("whitelisted channels already contains this channel, aborting")
            return
        elif guildDB.blacklistedChannels.__contains__(channelID):
            await ctx.reply("blacklisted channels already contains this channel, removing and adding to whitelist")
            guildDB.blacklistedChannels.remove(channelID)
            guildDB.whitelistedChannels.append(channelID)
            await guildDB.save()
        else:
            guildDB.whitelistedChannels.append(channelID)
            await ctx.message.add_reaction('✔')
            await guildDB.save()

    @commands.guild_only()
    @wlist.command(name='rm')
    @commands.has_guild_permissions(manage_guild=True)
    async def wlist_rm(self, ctx: commands.Context, channelID=None):
        channelID = int(channelID or ctx.channel.id)
        guildDB = await getOrCreateGuild(ctx.guild.id)
        if guildDB.whitelistedChannels.__contains__(channelID):
            guildDB.whitelistedChannels.remove(channelID)
            await guildDB.save()
            await ctx.message.add_reaction('✔')
            return
        else:
            await ctx.reply("Channel is not in whitelist")

    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.command(name="setupMessage")
    async def setupMessage(self, ctx: commands.Context):
        await util.setupGuild(self.bot, ctx.guild, ctx.author, ctx.channel)
        await ctx.message.add_reaction('✔')

    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.group(invoke_without_command=True)
    # lifted right from [letters](https://github.com/keli5/LettersBotPY/blob/master/cogs/owner.py) ty :3
    async def log(self, ctx: commands.Context):
        await ctx.reply("TODO: send current log status")

    @commands.guild_only()
    @log.command(name="setup")
    @commands.has_guild_permissions(manage_guild=True)
    async def log_setup(self, ctx: commands.Context):
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

    @commands.guild_only()
    @log.command(name="msg")
    @commands.has_guild_permissions(manage_guild=True)
    async def log_msg(self, ctx: commands.Context, messageID):
        messageID = int(messageID)
        after = await ctx.channel.fetch_message(messageID)
        guildDB = await getOrCreateGuild(after.guild.id)
        if not guildDB.unpinChannel:
            return
        embed = await formatMessage(after)
        await after.guild.get_channel(guildDB.unpinChannel).send(embed=embed)

    @commands.guild_only()
    @log.command(name="set")
    @commands.has_guild_permissions(manage_guild=True)
    async def log_set(self, ctx: commands.Context, arg1):
        arg1 = int(arg1)
        guildDB = await getOrCreateGuild(ctx.guild.id)
        guildDB.unpinChannel = arg1
        await guildDB.save()
        await ctx.message.add_reaction('✔')

    @commands.guild_only()
    @commands.group(invoke_without_command=True)
    @commands.has_guild_permissions(manage_guild=True)
    async def blist(self, ctx: commands.Context):
        await ctx.reply("Link to `blist` usage")

    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @blist.command(name='add')
    async def blist_add(self, ctx: commands.Context, channelID):
        channelID = channelID or ctx.channel.id
        channelID = int(channelID)
        guildDB = await getOrCreateGuild(ctx.guild.id)
        if guildDB.blacklistedChannels.__contains__(channelID):
            await ctx.send()
        if guildDB.whitelistedChannels.__contains__(channelID):
            await ctx.send("info: channel is already in whitelist\nremoving and adding to blacklist")
            guildDB.whitelistedChannels.remove(channelID)
        guildDB.blacklistedChannels.append(channelID)
        await guildDB.save()
        await ctx.message.add_reaction("✅")

    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @blist.command(name='rm')
    async def blist_rm(self, ctx: commands.Context, channelID):
        channelID = channelID or ctx.channel.id
        channelID = int(channelID)
        guildDB = await getOrCreateGuild(ctx.guild.id)
        if guildDB.blacklistedChannels.__contains__(channelID):
            guildDB.blacklistedChannels.remove(channelID)
            await ctx.message.add_reaction("✅")
            await guildDB.save()
        else:
            await ctx.send("the channel is not blacklisted, aborting")
            await ctx.message.add_reaction("❌")

    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.group(invoke_without_command=True)
    async def mode(self, ctx: commands.Context):
        await ctx.reply("[usage](https://github.com/sadanslargehole/neverForget/blob/master/_SETUP/modeUsage.md)")

    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @mode.command(name="set")
    async def mode_set(self, ctx: commands.Context, mode: str):
        if not mode:
            raise commands.MissingRequiredArgument(ctx.command.params['mode'])
        if mode.lower() == "wlist" or "whitelist":
            dbguild = await getOrCreateGuild(ctx.guild.id)
            dbguild.whitelist = True
            await dbguild.save()
            await ctx.message.add_reaction("✅")
        elif mode.lower() == "blist" or "blacklist":
            dbguild = await getOrCreateGuild(ctx.guild.id)
            dbguild.whitelist = False
            await dbguild.save()
            await ctx.message.add_reaction("✅")
        else:
            raise commands.BadArgument(mode)

    @commands.command(name="disable")
    @commands.has_guild_permissions(manage_guild=True)
    async def disable(self, ctx: commands.Context):
        guildDB = await getOrCreateGuild(ctx.guild.id)
        if guildDB.enabled:
            guildDB.enabled = False
            await guildDB.save()
            await ctx.message.add_reaction('✔')
            return
        else:
            await ctx.reply("the bot is already enabled")

    @commands.command(name='enable')
    @commands.has_guild_permissions(manage_guild=True)
    async def enable(self, ctx: commands.Context):
        guildDB = await getOrCreateGuild(ctx.guild.id)
        if guildDB.enabled:
            await ctx.reply("the bot is alreayd enabled")
            return
        result, message = await genEnableMessage(ctx.guild.id)
        if result:
            await ctx.send(message)
        else:
            await ctx.send(message)
            guildDB.enabled = True
            await guildDB.save()


async def setup(bot: commands.Bot):
    await bot.add_cog(adminCommands(bot))

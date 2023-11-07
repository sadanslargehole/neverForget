import datetime

import discord as d
import discord.abc
from discord.ext import commands
from util import getOrCreateGuild
from format import formatMessage, formatAndSend


class pinEvents(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener(name='on_message_edit')
    async def messageUnpin(self, before: d.Message, after: d.Message):
        if before.pinned and not after.pinned:
            # NOTE: the message was unpinned
            guildDB = await getOrCreateGuild(before.guild.id)
            if guildDB.enabled:
                if not guildDB.logAtPin:
                    # check whitelist mode
                    if guildDB.whitelist:
                        if guildDB.whitelistedChannels.__contains__(before.channel.id):
                            await formatAndSend(after, guildDB)
                    else:
                        if not guildDB.blacklistedChannels.__contains__(before.channel.id):
                            await formatAndSend(after, guildDB)
        elif not before.pinned and after.pinned:
            guildDB = await getOrCreateGuild(before.guild.id)
            if guildDB.enabled:
                if guildDB.logAtPin:
                    # check whitelist mode
                    if guildDB.whitelist:
                        if guildDB.whitelistedChannels.__contains__(before.channel.id):
                            await formatAndSend(after, guildDB)
                    else:
                        if not guildDB.blacklistedChannels.__contains__(before.channel.id):
                            await formatAndSend(after, guildDB)


async def setup(bot: commands.Bot):
    await bot.add_cog(pinEvents(bot))

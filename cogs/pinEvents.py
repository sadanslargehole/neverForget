import discord as d
from discord.ext import commands
from util import getOrCreateGuild
from classes.Models import guild
from format import formatMessage


class pinEvents(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener('on_message_edit')
    async def messageUnpin(self, before: d.Message, after: d.Message):
        if not (before.pinned and not after.pinned):
            return
        guildDB = await getOrCreateGuild(after.guild.id)
        if not guildDB.unpinChannel:
            return
        embed = await formatMessage(after)
        await after.guild.get_channel(guildDB.unpinChannel).send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(pinEvents(bot))

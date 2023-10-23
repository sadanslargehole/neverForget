import datetime
import discord as d
from discord.ext import commands
from typing import Union, Optional

class pinEvents(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener('on_message_edit')
    async def messageUnpin(self, before: d.Message, after:d.Message):
        if not (before.pinned and not after.pinned):
            return




async def setup(bot: commands.Bot):
    await bot.add_cog(pinEvents(bot))


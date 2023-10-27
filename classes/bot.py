from typing import Type

from discord import app_commands
from discord.ext import commands
import discord
from typing import *

from discord.ext.commands import errors


class bot(commands.Bot):
    config: dict[str, str]
    setup: dict[discord.User, discord.TextChannel]

    def __init__(
            self,
            command_prefix:str= "`",
            *,
            intents: discord.Intents = discord.Intents.all(),
            config: dict[str, str],
            **options: Any,
    ):
        super().__init__(command_prefix=command_prefix, intents=intents)

        self.config = config
    def on_command_error(self, context: commands.Context, exception: errors.CommandError, /) -> None:
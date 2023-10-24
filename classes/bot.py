from typing import Type

from discord import app_commands
from discord.ext import commands
import discord
from typing import *

from discord.ext.commands import HelpCommand
from discord.ext.commands._types import BotT
from discord.ext.commands.bot import PrefixType, _default


class bot(commands.Bot):
    config: dict[str, str]
    setup: dict[discord.User, discord.TextChannel]

    def __init__(
            self,
            command_prefix: PrefixType[BotT] = "`",
            *,
            help_command: Optional[HelpCommand] = _default,
            tree_cls: Type[app_commands.CommandTree[Any]] = app_commands.CommandTree,
            description: Optional[str] = None,
            intents: discord.Intents = discord.Intents.all(),
            config: dict[str, str],
            **options: Any,
    ):
        super().__init__(command_prefix=command_prefix, intents=intents)

        self.config = config
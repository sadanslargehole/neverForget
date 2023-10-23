from typing import Type

from discord import app_commands
from discord.ext import commands
import discord
from typing import *

from discord.ext.commands import HelpCommand
from discord.ext.commands._types import BotT
from discord.ext.commands.bot import PrefixType, _default
from Models import guild, user, db
from peewee import SqliteDatabase

from classes.Models import user, guild
from util import loadconfig


class bot(commands.Bot):
    guild_db: Type[guild]
    config: dict[str, str]
    user_db: Type[user]

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
        db.connect(True)
        db.create_tables([guild, user])
        self.user_db = user
        self.guild_db = guild
        self.config = config

    def getGuildOrNone(self, guildID: int):
        return self.guild_db.get_by_id(guildID)



    def getUserOrNone(self, userID: int):
        return self.user_db.get_by_id(userID)

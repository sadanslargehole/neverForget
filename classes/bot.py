from typing import Type
import difflib
from discord import app_commands
from discord.ext import commands
import discord
from typing import *

from discord.ext.commands import errors

cooldown_texts = ["Hey there.", "Hold on a second!", "pls wait...", "Cooldown..", "Hey, chill.",
                  "Just a minute...", "Give it a second.", "Whoop", "..."]


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

    # stolen from letters
    async def on_command_error(self, ctx: commands.Context, exe: errors.CommandError, /) -> None:
        delay = 10
        excname = type(exe).__name__
        errembed = discord.Embed(
            title=f"{excname} error",
            description=str(exe),
            color=0xAA0000
        )

        if isinstance(exe, commands.CommandNotFound):
            commandnames = []
            failed = str(exe).split(" ")
            failed = failed[1]
            parsedfailed = failed.replace("\"", "")

            for command in ctx.bot.commands:
                commandnames.append(command.name)
                for alias in command.aliases:
                    if alias == "":
                        return
                    commandnames.append(alias)

            matches = difflib.get_close_matches(parsedfailed, commandnames, 6, 0.5)
            if len(matches) == 0:
                return
            dymembed = discord.Embed(
                title=f"Couldn't find command {failed}",
                color=0xff0000,
                description="Did you mean..."
            )

            for match in matches:
                dymembed.add_field(name=f"{ctx.bot.command_prefix}{match}?", value="\u202d")

            await ctx.send(embed=dymembed)
            return

        if isinstance(exe, commands.MissingRequiredArgument):
            ctx.command.reset_cooldown(ctx)
        elif isinstance(exe, commands.CommandOnCooldown):
            errembed.title = random.choice(cooldown_texts)
        else:
            print(f"{excname}: {exe}")

        errmsg = await ctx.send(embed=errembed)
        await errmsg.delete(delay=delay)
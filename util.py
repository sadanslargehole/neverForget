from datetime import datetime
from json import load

import discord
from tortoise import Tortoise

import classes.bot


def loadconfig() -> dict[str, str]:
    with open('./config.json',"r" ) as cfg:
        return load(cfg)


async def initDB():
    await Tortoise.init(
        db_url='sqlite://neverforget_data.sqlite3',
        modules={'models': ["classes.Models"]}
    )
    # Generate the schema
    await Tortoise.generate_schemas(safe=True)


async def getInviterOrOwner(bot: classes.bot.bot, guild: discord.Guild) -> discord.User:
    integrations = await guild.integrations()
    user: discord.User | None = None
    if integrations:
        for i in integrations:
            if isinstance(i, discord.BotIntegration):
                if i.application.user.name == bot.user.name:
                    user = i.user
    if user is None:
        user = bot.get_user(guild.owner_id)
    return user


async def getChannelOrRand(guild: discord.Guild) -> discord.TextChannel:
    if guild.system_channel:
        return guild.system_channel
    else:
        channels = guild.channels
        for i in channels:
            if isinstance(i, discord.TextChannel):
                return i


async def setupGuild(bot: classes.bot.bot, guild: discord.Guild, user: discord.User | None = None, channel: discord.TextChannel = None):
    if not user:
        user = await getInviterOrOwner(bot, guild)
    if not channel:
        channel = getChannelOrRand(guild)
    embedWlistBlist = discord.Embed(title=f"{user.mention} Lets setup your bot",
                          description=f"Would you like whitelist or blacklist mode?\n**Whitelist mode**\nWhitelist mode only logs unpins in the channels you choose.\nTo add/remove a channel to/from the whitelist run {bot.config['prefix']}wlist <add|rm> [channel id].\n**Blacklist mode**\nLogs unpins in all channels except for the ones that you don't want.\nTo add/remove a channel to/from the blacklist run {bot.config['prefix']}blist <add|rm> [channel id].",
                          colour=0x00ff6e,
                          timestamp=datetime.now())

    embedWlistBlist.set_author(name="Setup your server!")

    embedWlistBlist.set_footer(text="Made by sadanslargehole :3",
                     icon_url="https://slate.dan.onl/slate.png")

    await guild.get_channel(channel.id).send(embed=embedWlistBlist, allowed_mentions=discord.AllowedMentions.users, )

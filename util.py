from datetime import datetime
from json import load

import discord
from tortoise import Tortoise
from classes.Models import guild

import classes.bot


def loadconfig() -> dict:
    with open('./config.json', "r") as cfg:
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


# FIXME - update setupGuild
async def setupGuild(bot: classes.bot.bot, guild: discord.Guild, user: discord.User | None = None, channel: discord.TextChannel = None):
    if not user:
        user = await getInviterOrOwner(bot, guild)
    if not channel:
        channel = getChannelOrRand(guild)

    await guild.get_channel(channel.id).send(content=f"{user.mention} \n# SETUP THE BOT HERE\nhttps://github.com/sadanslargehole/neverForget/blob/master/_SETUP/README.md", allowed_mentions=discord.AllowedMentions.users, )


async def getOrCreateGuild(gID: int) -> guild:
    toRet = await guild.get_or_create({
            'id': gID,
            "canUseBot": True,
            'unpinChannel': None,
            'enabled': False,
            'whitelist': None,
            'whitelistedChannels': [],
            'blacklistedChannels': [],
            'blacklistedUsers': []
        },

    )
    return toRet[0]


async def genDefaultGuild(gID: int) -> guild:
    return await guild.create(
            id=gID,
            canUseBot=True,
            unpinChannel=None,
            enabled=False,
            whitelist=None,
            whitelistedChannels=[],
            blacklistedChannels=[],
            blacklistedUsers=[]
    )

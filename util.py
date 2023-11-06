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
async def setupGuild(bot: classes.bot.bot, guild: discord.Guild, user: discord.User | None = None,
                     channel: discord.TextChannel = None):
    if not user:
        user = await getInviterOrOwner(bot, guild)
    if not channel:
        channel = getChannelOrRand(guild)
    await getOrCreateGuild(guild.id)
    await guild.get_channel(channel.id).send(
        content=f"{user.mention} \n# SETUP THE BOT HERE\nhttps://github.com/sadanslargehole/neverForget/blob/master/_SETUP/README.md",
        allowed_mentions=discord.AllowedMentions(users=True, replied_user=True, everyone=False, roles=False))


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


async def genEnableMessage(guildID: int) -> tuple[bool, str]:
    guildDB = await getOrCreateGuild(guildID)
    codeblockHeader = "```ansi"
    codeblockFooter = "```"
    modeInfoWhitelist = "[2;36mINFO - Mode is whitelist[0m\n"
    modeInfoUnpinChannel = "[2;36mINFO - Logging Channel: $CHANNEL$[0m\n"
    modeInfoBlacklist = "[2;36mINFO - Mode is blacklist[0m\n"
    whitelistedChannels = "[2;36mINFO - Whitelisted channels: $CHANNELS$[0m\n"
    blacklistedChannels = "[2;36mINFO - Blacklisted channels: $CHANNELS$[0m\n"
    warnNoBlacklistedChannels = "[2;33mWARN - Mode is blacklist and there are no blacklisted channels[0m\n"
    errorNoLogChannel = "[2;31mERROR - No logging channel set[0m\n"
    errorNoModeSet = "[2;31mERROR - No logging channel set[0m\n"
    errorNoWhitelistedChannels = "[2;31mERROR - Mode is whitelist and there are no whitelisted channels[0m\n"
    noErrorsFound = "[1;2mNo Errors Found, Logging Enabled[0m\n"
    errorsFound = "[2;41mErrors Found, Aborted[0m\n"
    message = codeblockHeader + "\n"
    errors = False
    if guildDB.unpinChannel:
        message += modeInfoUnpinChannel.replace("$CHANNEL$", guild.unpinChannel)
    else:
        errors = True
        message += errorNoLogChannel
    if guildDB.whitelist is None:
        message += errorNoModeSet
    elif guildDB.whitelist:
        message += modeInfoWhitelist
        if len(guildDB.whitelistedChannels) == 0:
            errors = True
            message += errorNoWhitelistedChannels
        else:
            message += whitelistedChannels.replace("$CHANNELS$", ", ".join(guildDB.whitelistedChannels))
    else:
        message += modeInfoBlacklist
        if len(guildDB.blacklistedChannels) == 0:
            message += warnNoBlacklistedChannels
        else:
            message += blacklistedChannels.replace("$CHANNELS$", ", ".join(guildDB.blacklistedChannels))
    if errors:
        message += errorsFound + codeblockFooter
    else:
        message += noErrorsFound + codeblockFooter
    return errors, message


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

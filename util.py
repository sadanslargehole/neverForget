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


async def getChannelOrRand(guildToGet: discord.Guild) -> discord.TextChannel:
    if guildToGet.system_channel:
        return guildToGet.system_channel
    else:
        channels = guildToGet.channels
        for i in channels:
            if isinstance(i, discord.TextChannel):
                return i
    raise Exception("fuck")


# FIXME - update setupGuild
async def setupGuild(bot: classes.bot.bot, joinedGuild: discord.Guild, user: discord.User | None = None,
                     channelToSendIn: discord.TextChannel = None):
    if not user:
        user = await getInviterOrOwner(bot, joinedGuild)
    if not channelToSendIn:
        channelToSendIn = await getChannelOrRand(joinedGuild)
    await getOrCreateGuild(joinedGuild.id)
    assert channelToSendIn is not None
    await channelToSendIn.send(
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
        pk=gID
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
    errorNoModeSet = "[2;31mERROR - No Mode Set[0m\n"
    errorNoWhitelistedChannels = "[2;31mERROR - Mode is whitelist and there are no whitelisted channels[0m\n"
    noErrorsFound = "[1;2mNo Errors Found, Logging Enabled[0m\n"
    errorsFound = "[2;41mErrors Found, Aborted[0m\n"
    message = codeblockHeader + "\n"
    errors = False
    if guildDB.whitelist is None:
        message += errorNoModeSet
    elif guildDB.whitelist:
        message += modeInfoWhitelist
        if len(guildDB.whitelistedChannels) == 0:
            errors = True
            message += errorNoWhitelistedChannels
        else:
            message += whitelistedChannels.replace("$CHANNELS$", guildDB.whitelistedChannels.__str__())
    else:
        message += modeInfoBlacklist
        if len(guildDB.blacklistedChannels) == 0:
            message += warnNoBlacklistedChannels
        else:
            message += blacklistedChannels.replace("$CHANNELS$", guildDB.blacklistedChannels.__str__())
    if guildDB.unpinChannel:
        message += modeInfoUnpinChannel.replace("$CHANNEL$", guildDB.unpinChannel.__str__())
    else:
        errors = True
        message += errorNoLogChannel
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


def paginate_list(list_items: list | tuple,
                  per_page: int = 10, page: int = 1) -> list:  # ?????
    page = page - 1
    start = (page * per_page)
    stop = start + per_page
    return list_items[start:stop]


def tally_users(bot) -> int:
    count = 0
    users_seen = []
    for eachGuild in bot.guilds:
        for member in eachGuild.members:
            if member.id not in users_seen:
                users_seen.append(member.id)
                count += 1
    return count

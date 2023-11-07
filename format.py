from datetime import datetime

import discord


async def formatMessage(m: discord.Message) -> discord.Embed:
    desc: str
    desc = m.content or m.attachments[0].filename or "error: could not load message content, please report this"

    if m.reference:
        context = ""
        if m.reference.cached_message:
            context = m.reference.cached_message.content
        else:
            tmp = await m.channel.fetch_message(m.reference.message_id)
            context = tmp.content
        desc = f"> {context}\n\n" + desc

    embed = discord.Embed(title=f"Original in #{m.channel.name}",
                          url=m.jump_url,
                          description=desc,
                          colour=0x00b0f4,
                          timestamp=m.created_at)

    embed.set_author(name=m.author.name,
                     url=f'https://discordapp.com/users/{m.author.id}',
                     icon_url=m.author.avatar.url)
    if m.attachments.__len__() > 0:
        for i in m.attachments:
            if i.content_type.__contains__("image"):
                embed.set_image(url=i.url)
                break

    embed.set_footer(text="made by sadanslargehole")
    return embed


async def formatAndSend(after, guildDB):
    embed = await formatMessage(after)
    await after.guild.get_channel(guildDB.unpinChannel).send(embed=embed)

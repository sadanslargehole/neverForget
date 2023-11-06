import discord
from discord.ext import commands
from discord.ext.commands import BucketType

import classes.bot
from classes.Models import guild
from cogs.adminCommands import guild_fields
from util import genDefaultGuild, getOrCreateGuild


class ownerCommands(commands.Cog):
    def __init__(self, bot: classes.bot.bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def enablebot(self, ctx: commands.Context):
        self.bot.enabled = True

    @commands.is_owner()
    @commands.command()
    async def disablebot(self, ctx: commands.Context):
        self.bot.enabled = False

    @commands.is_owner()
    @commands.command(aliases=['quit'])
    async def exit(self, ctx: commands.Context, *args):
        print(f"exited by {ctx.author.name} with reason:\n {' '.join(args)}")
        exit(0)

    @commands.is_owner()
    @commands.command(aliases=["dm", "msg"])
    async def message(self, ctx: commands.Context, target: int, *message):
        message = ' '.join(message)
        await self.bot.get_user(target).send(content=message)
        await ctx.message.add_reaction("✔")

    @commands.is_owner()
    @commands.group(invoke_without_command=True)
    async def db(self, ctx: commands.Context, *args):
        await ctx.reply("nope :3")

    @commands.command()
    @commands.is_owner()
    async def send(self, ctx: commands.Context, channelID: int, *args):
        await self.bot.get_channel(channelID).send(' '.join(args))
        await ctx.message.add_reaction("✔")

    @db.command(name='wipe')
    @commands.is_owner()
    # wipes and refreshed the guild db
    # TODO: fix this horror code
    async def db_wipe(self, ctx: commands.Context, guildID=None):
        guildID = guildID or ctx.guild.id
        guildID = int(guildID)
        await getOrCreateGuild(guildID)
        guildDB = await guild[guildID]
        await guildDB.delete()
        await getOrCreateGuild(guildID)
        await ctx.message.add_reaction("✔")

    @commands.is_owner()
    @db.command(name='get')
    async def db_get(self, ctx: commands.Context, guildID):
        guildID = guildID or ctx.guild.id
        guildID = int(guildID)
        guild_entry = await getOrCreateGuild(guildID)
        getEmbed = discord.Embed(
            title=f"Guild.{guildID}"
        )
        for field in guild_fields:
            attr = ""
            try:
                attr = getattr(guild_entry, field)
                if field == 'unpinChannel' and attr:
                    getEmbed.add_field(name=field, value=f'<#{attr}>')
                else:
                    getEmbed.add_field(name=field, value=attr)

            except AttributeError:
                pass
        await ctx.reply(embed=getEmbed)


async def setup(bot: classes.bot.bot):
    await bot.add_cog(ownerCommands(bot))

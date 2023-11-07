import discord
from discord.ext import commands
from discord.ext.commands import BucketType

import classes.bot
from classes.Models import guild
from cogs.adminCommands import guild_fields
from util import genDefaultGuild, getOrCreateGuild, paginate_list, tally_users


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
        await ctx.send("nope :3")

    @commands.command()
    @commands.is_owner()
    async def send(self, ctx: commands.Context, channelID: int, *args):
        await self.bot.get_channel(channelID).send(' '.join(args))
        await ctx.message.add_reaction("✔")

    @db.command(name='wipe')
    @commands.is_owner()
    # wipes and refreshed the guild db
    async def db_wipe(self, ctx: commands.Context, guildID=None):
        guildID = int(guildID or ctx.guild.id)
        guildDB = await guild.get_or_none(id=guildID)
        if guildDB:
            await guildDB.delete()
        await getOrCreateGuild(guildID)
        await ctx.message.add_reaction("✔")

    @commands.is_owner()
    @commands.group(invoke_without_command=True, name="get")
    async def get(self, ctx: commands.Context):
        await ctx.send_help()

    @commands.command()
    @commands.is_owner()
    async def guilds(self, ctx, page: int = 1, safe: bool = True):
        # guild.name, guild.id, guild.members, ctx.bot.guilds is amount of guilds, tally_users(ctx.bot)
        gembed = discord.Embed(
            title=f"Guilds (page {page}) ",
            color=discord.Color.blurple()
        )
        guilds = paginate_list(ctx.bot.guilds, 10, page)
        if len(guilds) == 0:
            return await ctx.send("That page doesn't exist!")
        for oneGuild in guilds:
            if safe:
                gembed.add_field(name=oneGuild.name, value=f"{oneGuild.member_count} members")  # ??
            else:
                gembed.add_field(name=f"{oneGuild.name} ({oneGuild.id})",
                                 value=f"{oneGuild.member_count} members, owned by {oneGuild.owner}")

        gembed.set_footer(text=f"{len(ctx.bot.guilds)} guilds, {tally_users(ctx.bot)} unique users")

        await ctx.send(embed=gembed)

    @commands.is_owner()
    @db.command(name='get')
    async def db_get(self, ctx: commands.Context, guildID=None):
        guildID = int(guildID or ctx.guild.id)
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

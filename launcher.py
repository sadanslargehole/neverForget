import traceback
from tortoise import run_async
import discord
from discord.ext import commands
from os import listdir
import asyncio
from util import loadconfig, initDB
from classes.bot import bot
# declare intents
# TODO: add proper intents
bot = bot(config=loadconfig())


async def load():
    blacklistedFiles = ["__pycache__", "template.py"]
    for i in listdir("cogs"):
        try:
            if blacklistedFiles.__contains__(i):
                continue
            i = i.removesuffix('.py')
            await bot.load_extension(f'cogs.{i}')
        except Exception as e:
            traceback.print_exception(e)
            print(f'error while loading {i}')
            exit(1)
        finally:
            print('loaded all cogs, no errors reported')
asyncio.run(load())
run_async(initDB())
bot.owner_id = bot.config['ownerID']
bot.run(bot.config['token'])

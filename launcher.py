#!/usr/bin/env python3
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

run_async(initDB())


async def load():
    blacklistedFiles = ["__pycache__", "template.py"]
    await bot.load_extension('jishaku')
    for i in listdir("cogs"):
        try:
            if blacklistedFiles.__contains__(i):
                i = ""
                continue
            i = i.removesuffix('.py')
            await bot.load_extension(f'cogs.{i}')
        except Exception as e:
            traceback.print_exception(e)
            print(f'error while loading {i}')
            exit(1)
        finally:
            print(f'loaded {i}')
    print('loaded all cogs, no errors reported')
asyncio.run(load())

bot.owner_id = bot.config['ownerID']
bot.run(bot.config['token'])

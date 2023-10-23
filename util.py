from json import load
from tortoise import Tortoise


def loadconfig() -> dict[str, str]:
    with open('./config.json',"r" ) as cfg:
        return load(cfg)


async def init():
    await Tortoise.init(
        db_url='sqlite://neverforget_data.sqlite3',
        modules={'models': ["classes.Models"]}
    )
    # Generate the schema
    await Tortoise.generate_schemas(safe=True)

from dotenv import load_dotenv
from os import getenv

from source.internal import Bot

load_dotenv()

bot = Bot()

bot.load_extensions(
    "jishaku",
    "source.cogs.rooms",
)

bot.run(getenv("TOKEN"))
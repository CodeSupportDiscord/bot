from dotenv import load_dotenv
from os import getenv

from source.internal import Bot

load_dotenv()

bot = Bot()

bot.load_extensions(
    "jishaku",
)

bot.run(getenv("TOKEN"))
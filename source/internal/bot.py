from discord.ext import commands
from discord import Message, Intents
from aiohttp import ClientSession
from typing import Optional
from traceback import format_exc


class Bot(commands.Bot):
    """A subclass of `commands.Bot` with additional features."""

    def __init__(self, *args, **kwargs):
        intents = Intents.all()

        super().__init__(
            command_prefix=self.get_prefix,
            intents=intents,
            *args,
            **kwargs,
        )

        self.http_session: Optional[ClientSession] = None

    def load_extensions(self, *exts):
        """Load a set of extensions, autoprefixed by 'cogs.'"""
        for ext in exts:
            try:
                self.load_extension(f"cogs.{ext}")
                self.logger.info(f"Loaded cog cogs.{ext}")
            except Exception:
                self.logger.error(f"Failed to load cog: cogs.{ext}: {format_exc()}")

    async def login(self, *args, **kwargs) -> None:
        """Create the aiohttp ClientSession before logging in."""

        self.http_session = ClientSession()

        await super().login(*args, **kwargs)

    async def get_prefix(self, message: Message) -> str:
        """Get a dynamic prefix for the bot."""

        return ">"

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
            command_prefix="!",
            intents=intents,
            *args,
            **kwargs,
        )

        self.http_session: Optional[ClientSession] = None

    def load_extensions(self, *exts):
        """Load a set of extensions."""
        for ext in exts:
            try:
                self.load_extension(ext)
                print(f"Loaded cog {ext}")
            except Exception:
                print(f"Failed to load cog: {ext}: {format_exc()}")

    async def login(self, *args, **kwargs) -> None:
        """Create the aiohttp ClientSession before logging in."""

        self.http_session = ClientSession()

        await super().login(*args, **kwargs)

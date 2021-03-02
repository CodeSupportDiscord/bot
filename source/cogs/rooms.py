from discord.ext import commands
from discord import CategoryChannel, Embed, File
from async_rediscache import RedisCache
from asyncio import Lock
from os import getenv
from typing import Optional
from io import StringIO

from source.internal import Bot

def has_no_room():
    async def predicate(ctx: commands.Context):
        return not await ctx.cog.cache.contains(ctx.author.id)
    return commands.check(predicate)

def is_own_room():
    async def predicate(ctx: commands.Context):
        user_room = await ctx.cog.cache.get(ctx.author.id)
        return bool(user_room)
    return commands.check(predicate)


class Rooms(commands.Cog):
    """Automatically manage user help rooms."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.cache = RedisCache(namespace="rooms")
        self.cat: Optional[CategoryChannel]

        self.ready = False

    @commands.Cog.listener()
    async def on_ready(self):
        self.cat = self.bot.get_channel(int(getenv("ROOMS")))
        self.ready = True
        print("Rooms is ready to go!")

    @commands.command(name="room")
    @has_no_room()
    async def create_room(self, ctx: commands.Context):
        """Create a new help room."""

        if not self.ready:
            return await ctx.send("The bot isn't ready to handle your request, please try again in a few seconds.")

        def check(reaction, user):
            return user.id == ctx.author.id and str(reaction.emoji) in ["✅", "🛑"]

        message = await ctx.send("Are you sure you want to create a help room?")
        await message.add_reaction("✅")
        await message.add_reaction("🛑")

        try:
            reaction, _ = await self.bot.wait_for("reaction", check=check, timeout=30)
        except:
            return await message.edit(content="Help room creation cancelled.")

        if str(reaction.emoji) != "✅":
            return await message.edit(content="Help room creation cancelled.")

        channel = await self.cat.create_text_channel(name=str(ctx.author))
        await self.cache.set(ctx.author.id, channel.id)

        message = await channel.send(f"This help room has been created for {ctx.author.mention} - please read <#816027169612234762> before helping.")
        await message.pin()
        await ctx.message.add_reaction("✅")

    @commands.command(name="close")
    @is_own_room()
    async def close_room(self, ctx: commands.Context):
        """Close your own help room."""

        messages = await ctx.channel.history(limit=None, oldest_first=True).flatten()

        embed_message = None
        content = ""
        for message in messages:
            if message.author == ctx.author and not embed_message:
                embed_message = message.content
            content += f"{message.author}: {message.content}\n\n"

        await self.cache.delete(ctx.author.id)
        await ctx.channel.delete()
        if embed_message == "!close" or not embed_message:
            return

        logs = self.bot.get_channel(int(getenv("ROOM_LOGS")))
        embed = Embed(colour=0x87CEEB, description=embed_message)
        embed.set_author(name=f"{ctx.author} | Help", icon_url=str(ctx.author.avatar_url))

        await logs.send(embed=embed, file=File(StringIO(content), str(ctx.author.id)))


def setup(bot: Bot):
    bot.add_cog(Rooms(bot))
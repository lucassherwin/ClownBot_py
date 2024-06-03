"""Helper functions for ClownBot"""

import logging
import time

from discord.ext.commands import Context
from discord.guild import Guild

from clown_bot.bot import ClownData
from clown_bot.config import Config

logger = logging.getLogger("ClownBot")


def is_clown_admin(ctx: Context) -> bool:
    """
    Check if a message author is a specified clown admin
    :param ctx: Discord Context object
    :return: Boolean
    """
    return ctx.author.id in Config().admin_ids


def get_members(guild: Guild):
    """
    Log the list of members in given server
    :param guild: Discord Guild object
    """
    members = "\n - ".join([member.name for member in guild.members])
    logger.info(f"Guild Members:\n - {members}")


async def get_display_name(ctx: Context, clown_id: int, clown_data: ClownData) -> str:
    """
    Pull given account id's display name in server that the command was called from.

    First checks the name cache, and then refreshes the cache if expired.

    :param ctx: Discord Context object
    :param clown_id: Discord account ID to return display name of
    :return: Display name of given id
    """
    s = Config()
    guild_id = str(ctx.guild.id)

    # Check if guild not cached or if cache has expired, and reacquire display names if so
    if (
        guild_id not in clown_data.name_cache.keys()
        or float(clown_data.name_cache[guild_id]["expiration_time"])
        + s.name_cache_ttl_seconds
        <= time.time()
    ):
        clown_data.name_cache[guild_id] = {
            "expiration_time": time.time() + s.name_cache_ttl_seconds,
            "members": {},
        }

        async for member in ctx.guild.fetch_members(limit=None):
            clown_data.name_cache[guild_id]["members"][member.id] = member.display_name
    return clown_data.name_cache[guild_id]["members"][clown_id]


def is_wordle_channel(channel_name: str) -> bool:
    """
    Check if "wordle" appears in channel name at all
    :param channel_name: String channel name
    :return: Bool
    """
    return "wordle" in channel_name.lower()

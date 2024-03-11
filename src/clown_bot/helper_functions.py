"""Helper functions for ClownBot"""

import json
import time

from discord.ext.commands import Context
from discord.guild import Guild

from clown_bot.bot import ClownData


def is_clown_admin(ctx: Context) -> bool:
    """
    Check if a message author is a specified clown admin
    :param ctx: Discord Context object
    :return: Boolean
    """
    admin_ids = [
        114384475743453193,  # Nick
        114338477922975745  # Lucas
    ]
    return ctx.author.id in admin_ids


def get_members(guild: Guild):
    """
    Print list of members in given server
    :param guild: Discord Guild object
    """
    members = "\n - ".join([member.name for member in guild.members])
    print(f"Guild Members:\n - {members}")


def sort_leaderboard(clown_data: ClownData, guild_id: str):
    """
    Sort leaderboard for given guild id by values
    :param guild_id: Guild id to sort leaderboard for
    """
    clown_data.leaderboard[guild_id] = dict(
        sorted(clown_data.leaderboard[guild_id].items(),
               key=lambda item: item[1],
               reverse=True))


def save_leaderboard(clown_data: ClownData):
    """
    Write leaderboard to file
    """
    with open(clown_data.clown_file, "w", encoding="utf-8") as out_file:
        json.dump(clown_data.leaderboard, out_file)


async def get_display_name(ctx: Context, clown_id: str, clown_data: ClownData) -> str:
    """
    Pull given account id's display name in server that the command was called from.
    
    First checks the name cache, and then refreshes the cache if expired.

    :param ctx: Discord Context object
    :param clown_id: Discord account ID to return display name of
    :return: Display name of given id
    """
    guild_id = str(ctx.guild.id)

    # Check if guild not cached or if cache has expired, and reacquire display names if so
    cache_ttl_seconds = 600
    if guild_id not in clown_data.name_cache.keys() or float(
            clown_data.name_cache[guild_id]["time"]) + cache_ttl_seconds < time.time():
        clown_data.name_cache[guild_id] = {"time": time.time(), "members": {}}

        async for member in ctx.guild.fetch_members(limit=None):
            clown_data.name_cache[guild_id]["members"][str(
                member.id)] = member.display_name

        with open(clown_data.name_cache_file, "w", encoding="utf-8") as out_file:
            json.dump(clown_data.name_cache, out_file)
    return clown_data.name_cache[guild_id]["members"][clown_id]


def is_wordle_channel(channel_name: str) -> bool:
    """
    Check if "wordle" appears in channel name at all
    :param channel_name: String channel name
    :return: Bool
    """
    return "wordle" in channel_name.lower()

import global_
import json
import time


def is_clown_admin(ctx):
    """
    Check if a message author is a specified clown admin
    :param ctx: Discord Context object
    :return: Boolean
    """
    admin_ids = [
        114384475743453193,   # Nick
        114338477922975745    # Lucas
    ]
    return ctx.author.id in admin_ids


def get_members(guild):
    """
    Print list of members in given server
    :param guild: Discord Guild object
    """
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


def sort_leaderboard(guild_id):
    """
    Sort leaderboard for given guild id by values
    :param guild_id: Guild id to sort leaderboard for
    """
    global_.leaderboard[guild_id] = {k: v for k, v in sorted(
        global_.leaderboard[guild_id].items(), key=lambda item: item[1], reverse=True)}


def save_leaderboard():
    """
    Write leaderboard to file
    """
    with open(global_.clown_file, 'w') as out_file:
        json.dump(global_.leaderboard, out_file)


async def get_display_name(ctx, clown_id):
    """
    Pull given account id's display name in server that the command was called from, from the name cache, and refresh
    cache if expired
    :param ctx: Discord Context object
    :param clown_id: Discord account ID to return display name of
    :return: Display name of given id
    """
    guild_id = str(ctx.guild.id)

    # Check if guild not cached or if cache has expired, and reacquire display names if so
    cache_TTL_seconds = 600
    if guild_id not in global_.name_cache.keys() or float(global_.name_cache[guild_id]["time"]) + cache_TTL_seconds < time.time():
        global_.name_cache[guild_id] = {"time": time.time(), "members": {}}
        async for member in ctx.guild.fetch_members(limit=None):
            global_.name_cache[guild_id]["members"][str(member.id)] = member.display_name
        with open(global_.name_cache_path, 'w') as out_file:
            json.dump(global_.name_cache, out_file)
    return global_.name_cache[guild_id]["members"][clown_id]

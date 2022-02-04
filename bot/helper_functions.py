import global_
import json


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

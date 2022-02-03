import discord
from discord.ext import commands
import helper_functions
import global_


def setup(bot):
  """
  Required setup function implicitly called by bot.load_extension in main bot file.
  Registers all commands in the bot.
  :param bot:
  """
  bot.add_command(test)
  bot.add_command(gamer)
  bot.add_command(clowns)
  bot.add_command(clownset)


@commands.command()
async def test(ctx):
  """
  Test command
  :param ctx: Discord Context object
  """
  print(global_.leaderboard)
  await ctx.send("test")


@commands.command()
async def gamer(ctx):
  """
  Call the command sender a Gamer
  :param ctx: Discord Context object
  """
  await ctx.send(f"{ctx.author} is a Gamer")


@commands.command()
async def clowns(ctx):
  """
  Send a discord embed containing the clown leaderboard information for the server the command was called from
  :param ctx: Discord Context object
  """
  # https://discordpy.readthedocs.io/en/latest/api.html?highlight=embed#discord.Embed
  # create an embed from the leaderboard obj
  guild_id = str(ctx.guild.id)
  try:
    embed = discord.Embed()
    embed.title = 'Biggest Clowns'
    for clownID in global_.leaderboard[guild_id]:
      clown = await ctx.guild.fetch_member(clownID)
      embed.add_field(
        name=f'**{clown.display_name}**', value=f'> Clowns: {global_.leaderboard[guild_id][clownID]}\n', inline=False)
    await ctx.channel.send(embed=embed)
  except KeyError:
    await ctx.channel.send("No clowns yet!")


@commands.command()
async def clownset(ctx, clown_id: str, clown_num: int):
  """
  Forcibly set a given user's clown count for the server that command is called from. Can only be called from specific
  discord accounts.
  :param ctx: Discord Context object
  :param clown_id: Discord account ID of user to modify
  :param clown_num: Number to set clown count to
  """
  # Nick and Lucas discord account id's
  valid_ids = [114384475743453193, 114338477922975745]
  if ctx.author.id not in valid_ids:
    await ctx.channel.send('You are not permitted to do this!')
    return
  guild_id = str(ctx.guild.id)
  if str(ctx.guild.id) not in global_.leaderboard.keys():
    global_.leaderboard[guild_id] = {}
  global_.leaderboard[guild_id][clown_id] = clown_num
  helper_functions.sort_leaderboard(guild_id)
  helper_functions.save_leaderboard()




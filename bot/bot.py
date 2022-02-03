import os
import discord
from discord.ext import commands
import json
from dotenv import load_dotenv
import pathlib
import helper_functions
import global_

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
# GUILD = os.getenv('DISCORD_GUILD')
# a client is an object that represents a connection to DIscord
# handles events, tracks state, and interacts with Discord APIs
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

file_directory = pathlib.Path(__file__).parent.resolve()
global_.clown_file = f"{file_directory}/clowns.json"

# open the clowns.json file and read in the data
with open(global_.clown_file) as json_file:
  global_.leaderboard = json.load(json_file)


# https://discordpy.readthedocs.io/en/latest/api.html#discord.RawReactionActionEvent
# https://discordpy.readthedocs.io/en/latest/api.html#discord.on_reaction_add
# https://discordpy.readthedocs.io/en/latest/api.html#discord.abc.Messageable
# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Context.fetch_message
# method to watch reactions
# payload has properties:
  # channel_id: The channel ID where the reaction got added or removed.
  # emoji: The custom or unicode emoji being used.
  # event_type: The event type that triggered this action. Can be REACTION_ADD for reaction addition or REACTION_REMOVE for reaction removal.
  # guild_id: The guild ID where the reaction got added or removed, if applicable.
  # member: The member who added the reaction. Only available if event_type is REACTION_ADD and the reaction is inside a guild.
  # message_id: The message ID that got or lost a reaction.
  # user_id: The user ID who added the reaction or whose reaction was removed.
@bot.event
async def on_raw_reaction_add(payload):
  # check to see if an emoji is added and that emoji is 🤡
  if str(payload.emoji) == '🤡':
    # get the channel to send a message to
    channel = bot.get_channel(payload.channel_id)
    # get the id of the message reacted to
    m_id = payload.message_id
    # get the id of the guild the message is in
    g_id = str(payload.guild_id)
    # fetch the message with the id
    message = await channel.fetch_message(m_id)
    sender = str(message.author)
    sender = sender.split('#')[0]
    # if the sender is ClownBot do nothing
    if sender == 'ClownBot_py':
      return
    if g_id not in global_.leaderboard.keys():
      global_.leaderboard[g_id] = {}
    # check for that user in the leaderboard obj
    # if the user is already in the leaderboard
    author_id = str(message.author.id)
    if author_id in global_.leaderboard[g_id].keys():
      global_.leaderboard[g_id][author_id] += 1
    # the user is not already in the leaderboard
    else:
      global_.leaderboard[g_id][author_id] = 1
    helper_functions.sort_leaderboard(g_id)
    helper_functions.save_leaderboard()
    print(global_.leaderboard)


# on_ready() handles the event when the Client has established a connection to Discord
@bot.event
async def on_ready():
  print('Running ClownBot...')

bot.load_extension("clown_commands")
bot.run(TOKEN)

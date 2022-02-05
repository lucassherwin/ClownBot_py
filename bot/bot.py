import os
import discord
from discord.ext import commands
import json
from dotenv import load_dotenv
import pathlib
import global_
import clown_commands

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
global_.name_cache_path = f"{file_directory}/name_cache.json"

# open the clowns.json file and read in the data
with open(global_.clown_file) as json_file:
  global_.leaderboard = json.load(json_file)

with open(global_.name_cache_path, 'r') as json_file:
  global_.name_cache = json.load(json_file)

# on_ready() handles the event when the Client has established a connection to Discord
@bot.event
async def on_ready():
  print('Running ClownBot...')

bot.add_cog(clown_commands.ClownInfo(bot))
bot.add_cog(clown_commands.General(bot))
bot.add_cog(clown_commands.Wordle(bot))
bot.run(TOKEN)

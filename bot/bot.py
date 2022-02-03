
import os
import discord
from discord.ext import commands
import json
from dotenv import load_dotenv
import pathlib

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
# GUILD = os.getenv('DISCORD_GUILD')
# a client is an object that represents a connection to DIscord
# handles events, tracks state, and interacts with Discord APIs
intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

file_directory = pathlib.Path(__file__).parent.resolve()
clown_file = f"{file_directory}/clowns.json"
# obj to contain the leaderboard
# {username: clown_score}
# after updating sort based on clown_score
leaderboard = {}
# open the clowns.json file and read in the data
with open(clown_file) as json_file:
    leaderboard = json.load(json_file)

# method to save the current leaderboard to the json


def save_leaderboard():
    global leaderboard

    with open(clown_file, 'w') as outfile:
        json.dump(leaderboard, outfile)


def sort_leaderboard(guild_id):
    global leaderboard
    leaderboard[guild_id] = {k: v for k, v in sorted(
        leaderboard[guild_id].items(), key=lambda item: item[1], reverse=True)}

# gets the members
# currently the only member listed is the clown bot
# not sure if this is supposed to list all the server members


def getMemebers(guild):
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

# various message commands


@client.event
async def on_message(message):
    global leaderboard
    # this gets the name of the person who sent the message
    sender = str(message.author)
    sender = sender.split('#')[0]
    # Client cant tell the difference between a bot and a user
    # Therefore we include this if to check if the bot is reacting to its own message
    if message.author == client.user:
        return
    if message.content == '!test':
        print(leaderboard)
        await message.channel.send('test')
    if message.content == '!gamer':
        await message.channel.send('{} is a Gamer'.format(sender))
    # leaderboard command
    if message.content == '!clowns':
        # https://discordpy.readthedocs.io/en/latest/api.html?highlight=embed#discord.Embed
        # create an embed from the leaderboard obj
        guild_id = str(message.guild.id)

        try:
            embed = discord.Embed()
            embed.title = 'Biggest Clowns'
            for clownID in leaderboard[guild_id]:
                clown = await message.guild.fetch_member(clownID)
                embed.add_field(
                    name=f'**{clown.display_name}**', value=f'> Clowns: {leaderboard[guild_id][clownID]}\n', inline=False)
            await message.channel.send(embed=embed)
        except KeyError:
            await message.channel.send("No clowns yet!")
        return

    # Manually set clown count for user, only allowed from Nick or Lucas's accounts
    # First parameter is discord account id, second parameter is number of clowns
    if message.content[:9] == '!clownset':
        valid_ids = [114384475743453193, 114338477922975745]    # Nick and Lucas discord account id's
        if message.author.id not in valid_ids:
            return
        args = message.content.split()
        if len(args) < 3:
            await message.channel.send("Not enough arguments")
            return
        guild_id = str(message.guild.id)
        clown_id = args[1]
        clown_count = int(args[2])
        if str(message.guild.id) not in leaderboard.keys():
            leaderboard[guild_id] = {}
        leaderboard[guild_id][str(clown_id)] = clown_count
        sort_leaderboard(guild_id)
        save_leaderboard()


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
@client.event
async def on_raw_reaction_add(payload):
    global leaderboard
    # check to see if an emoji is added and that emoji is 🤡
    if str(payload.emoji) == '🤡':
        # get the channel to send a message to
        channel = client.get_channel(payload.channel_id)
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
        if g_id not in leaderboard.keys():
            leaderboard[g_id] = {}
        # check for that user in the leaderboard obj
        # if the user is already in the leaderboard
        author_id = str(message.author.id)
        if author_id in leaderboard[g_id].keys():
            leaderboard[g_id][author_id] += 1
        # the user is not already in the leaderboard
        else:
            leaderboard[g_id][author_id] = 1
        sort_leaderboard(g_id)
        save_leaderboard()
        print(leaderboard)

# on_ready() handles the event when the Client has established a connection to Discord


@client.event
async def on_ready():
    # gets the server using built in discord get() function
    #guild = discord.utils.get(client.guilds, name=GUILD)
    print('Running ClownBot...')

client.run(TOKEN)

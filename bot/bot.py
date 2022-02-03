
import os
import discord
from discord.ext import commands
import json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
# a client is an object that represents a connection to DIscord
# handles events, tracks state, and interacts with Discord APIs
client = discord.Client()

# obj to contain the leaderboard
# {username: clown_score}
# after updating sort based on clown_score
leaderboard = {}
# open the clowns.json file and read in the data
with open('./bot/clowns.json') as json_file:
    leaderboard = json.load(json_file)

# method to save the current leaderboard to the json


def save_leaderboard():
    global leaderboard

    with open('./clowns.json', 'w') as outfile:
        json.dump(leaderboard, outfile)


def sort_leaderboard():
    global leaderboard
    leaderboard = {k: v for k, v in sorted(
        leaderboard.items(), key=lambda item: item[1], reverse=True)}

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
        embed = discord.Embed.from_dict(leaderboard)
        embed.title = 'Biggest Clowns'
        for clown in leaderboard:
            embed.add_field(
                name=f'**{clown}**', value=f'> Clowns: {leaderboard[clown]}\n', inline=False)
        await message.channel.send(embed=embed)


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
        # fetch the message with the id
        message = await channel.fetch_message(m_id)
        sender = str(message.author)
        sender = sender.split('#')[0]
        # if the sender is ClownBot do nothing
        if sender == 'ClownBot_py':
            return
        # check for that user in the leaderboard obj
        # if the user is already in the leaderboard
        elif sender in leaderboard:
            leaderboard[sender] += 1
            sort_leaderboard()
            save_leaderboard()
            print(leaderboard)
        # the user is not already in the leaderboard
        else:
            leaderboard[sender] = 1
            sort_leaderboard()
            save_leaderboard()
            print(leaderboard)

# on_ready() handles the event when the Client has established a connection to Discord


@client.event
async def on_ready():
    # gets the server using built in discord get() function
    guild = discord.utils.get(client.guilds, name=GUILD)
    print('Running ClownBot...')

client.run(TOKEN)

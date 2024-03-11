"""Commands and listeners for Clown interactions."""

import logging

import discord
from discord.ext.commands import CheckFailure, Cog, Context, check, command

from clown_bot.bot import ClownBot
from clown_bot.helper_functions import (get_display_name, is_clown_admin,
                                        save_leaderboard, sort_leaderboard)

logger = logging.getLogger("ClownBot")


class ClownInfo(Cog):
    """
    Commands pertaining to clowns
    """

    def __init__(self, bot: ClownBot):
        self.bot = bot

    # https://discordpy.readthedocs.io/en/latest/api.html#discord.RawReactionActionEvent
    @Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """
        Handle clown reactions
        """
        # check to see if an emoji is added and that emoji is 🤡
        if str(payload.emoji) == "🤡":
            # get the channel to send a message to
            channel = self.bot.get_channel(payload.channel_id)

            # get the id of the message reacted to
            m_id = payload.message_id

            # get the id of the guild the message is in
            g_id = str(payload.guild_id)

            # fetch the message with the id
            message = await channel.fetch_message(m_id)
            if message.author == self.bot.user:
                return

            if g_id not in self.bot.clown_data.leaderboard.keys():
                self.bot.clown_data.leaderboard[g_id] = {}
            # check for that user in the leaderboard obj
            # if the user is already in the leaderboard
            author_id = str(message.author.id)
            if author_id in self.bot.clown_data.leaderboard[g_id].keys():
                self.bot.clown_data.leaderboard[g_id][author_id] += 1
            # the user is not already in the leaderboard
            else:
                self.bot.clown_data.leaderboard[g_id][author_id] = 1
            sort_leaderboard(self.bot.clown_data, g_id)
            save_leaderboard(self.bot.clown_data)
            logger.debug(self.bot.clown_data.leaderboard)

    @command()
    async def clowns(self, ctx: Context):
        """
        Send a discord embed containing the clown leaderboard information for the server
        the command was called from.

        :param ctx: Discord Context object
        """
        # https://discordpy.readthedocs.io/en/latest/api.html?highlight=embed#discord.Embed
        # create an embed from the leaderboard obj
        guild_id = str(ctx.guild.id)
        if guild_id not in self.bot.clown_data.leaderboard:
            await ctx.channel.send("No clowns yet!")
            return

        embed = discord.Embed()
        embed.title = "Biggest Clowns"
        for clown_id in self.bot.clown_data.leaderboard[guild_id]:
            clown_name = await get_display_name(ctx, clown_id, self.bot.clown_data)
            embed.add_field(
                name=f"**{clown_name}**",
                value=f"> Clowns: {self.bot.clown_data.leaderboard[guild_id][clown_id]}\n",
                inline=False)
        await ctx.channel.send(embed=embed)
        logger.debug(
            f"Sent clown leaderboard to Guild {ctx.guild.id}, Channel {ctx.channel.id}")

    @command(hidden=True)
    @check(is_clown_admin)
    async def clownset(self, ctx: Context, clown_id: str, clown_num: int):
        """
        Forcibly set a given user's clown count for the invoking server. 
        Can only be called from specific discord accounts.
        
        :param ctx: Discord Context object
        :param clown_id: Discord account ID of user to modify
        :param clown_num: Number to set clown count to
        """

        guild_id = str(ctx.guild.id)
        if guild_id not in self.bot.clown_data.leaderboard.keys():
            self.bot.clown_data.leaderboard[guild_id] = {}
        self.bot.clown_data.leaderboard[guild_id][clown_id] = clown_num
        sort_leaderboard(self.bot.clown_data, guild_id)
        save_leaderboard(self.bot.clown_data)

    @clownset.error
    async def clownset_error(self, ctx: Context, error):
        """Handle errors for `clownset` command"""
        if isinstance(error, CheckFailure):
            await ctx.send("Hey, that's illegal")

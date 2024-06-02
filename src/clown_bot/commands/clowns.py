"""Commands and listeners for Clown interactions."""

import logging

import discord
from discord.ext.commands import CheckFailure, Cog, Context, check, command

from clown_bot.bot import ClownBot
from clown_bot.db import get_clowns, increment_clown, set_clown
from clown_bot.helper_functions import (
    get_display_name,
    is_clown_admin,
)

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
            # Fetch the channel the message was sent in
            channel = self.bot.get_channel(payload.channel_id)

            # Fetch the clowned messaage
            message = await channel.fetch_message(payload.message_id)

            guild_id = str(payload.guild_id)
            increment_clown(self.bot.db, guild_id, message.author.id)
            logger.debug(self.bot.clown_data)

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
        clowns = get_clowns(self.bot.db, guild_id)
        if not clowns:
            await ctx.channel.send("No clowns yet!")
            return

        embed = discord.Embed()
        embed.title = "Biggest Clowns"
        for clown in clowns:
            clown_name = await get_display_name(ctx, clown.id, self.bot.clown_data)
            embed.add_field(
                name=f"**{clown_name}**",
                value=f"> Clowns: {clown.count}\n",
                inline=False,
            )
        await ctx.channel.send(embed=embed)
        logger.debug(
            f"Sent clown leaderboard to Guild {ctx.guild.id}, Channel {ctx.channel.id}"
        )

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
        set_clown(self.bot.db, guild_id, int(clown_id), clown_num)

    @clownset.error
    async def clownset_error(self, ctx: Context, error):
        """Handle errors for `clownset` command"""
        if isinstance(error, CheckFailure):
            await ctx.send("Hey, that's illegal")

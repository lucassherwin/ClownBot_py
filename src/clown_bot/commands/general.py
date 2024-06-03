"""General-use commands"""

import logging

from discord.ext.commands import Cog, Context, command

from clown_bot.bot import ClownBot

logger = logging.getLogger("ClownBot")


class General(Cog):
    """
    Misc. commands
    """

    def __init__(self, bot: ClownBot):
        self.bot = bot

    @command()
    async def test(self, ctx: Context):
        """
        Test command
        :param ctx: Discord Context object
        """
        logger.debug(self.bot.clown_data)
        await ctx.send("test")

    @command()
    async def gamer(self, ctx: Context):
        """
        Call the command sender a Gamer
        :param ctx: Discord Context object
        """
        await ctx.send(f"{ctx.author} is a Gamer")

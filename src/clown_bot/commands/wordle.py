"""Commands and listeners pertaining to Wordle"""
import logging
import re

from discord import Message
from discord.ext.commands import Cog

from clown_bot.bot import ClownBot
from clown_bot.helper_functions import is_wordle_channel

logger = logging.getLogger("ClownBot")


class Wordle(Cog):
    """
    Commands and listeners pertaining to Wordle
    """

    wordle_regex = re.compile(r"Wordle \d+ X/\d", re.IGNORECASE)

    def __init__(self, bot: ClownBot):
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        """
        Check if user posted a failed wordle attempt in a wordle channel, and clown them if so
        :param message:
        """
        if message.author == self.bot:
            return
        if is_wordle_channel(message.channel.name):
            if re.match(self.wordle_regex, message.content):
                await message.add_reaction("🤡")
                logger.debug(f"Clowned {message.author} for failed wordle attempt")

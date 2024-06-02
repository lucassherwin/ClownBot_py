"""ClownBot class definition"""

import logging
from dataclasses import dataclass
from typing import Optional

from discord.ext.commands import Bot

from clown_bot.db import get_database

logger = logging.getLogger("ClownBot")


@dataclass
class ClownData:
    """ClownBot-specfic global data.

    Attributes:
        name_cache: dict: Cache of display names for users
    """

    def __init__(self, name_cache: Optional[dict[str, dict[str, dict]]] = None):
        self.name_cache = name_cache or {}


class ClownBot(Bot):
    """Subclass of the Discord Bot class with additional ClownBot-specific attributes."""

    def __init__(self, clown_data: ClownData, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clown_data: ClownData = clown_data
        self.db = get_database()

    async def on_ready(self):
        """ "Ready event handler"""
        logger.info(
            f"Logged in as `{self.user}` with ID `{self.user.id}`. Running ClownBot..."
        )

"""ClownBot class definition"""

import logging
import os
from dataclasses import dataclass
from typing import Dict, Optional

from discord.ext.commands import Bot

logger = logging.getLogger("ClownBot")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(os.environ.get("LOGLEVEL", "INFO").upper())


@dataclass
class ClownData:
    """ClownBot-specfic global data.

    Attributes:
        clown_file: str: Path to the file to store clown leaderboard
        name_cache_file: str: Path to the file to store name cache
        leaderboard: Dict[str, Dict]: Leaderboard for clowns in each server
        name_cache: dict: Cache of display names for users
    """

    def __init__(self,
                 clown_file: str,
                 name_cache_file: str,
                 leaderboard: Optional[Dict[str, Dict]] = None,
                 name_cache: Optional[Dict[str, Dict[str, Dict]]] = None):
        self.clown_file = clown_file
        self.name_cache_file = name_cache_file
        self.leaderboard = leaderboard or {}
        self.name_cache = name_cache or {}


class ClownBot(Bot):
    """Subclass of the Discord Bot class with additional ClownBot-specific attributes."""

    def __init__(self, clown_data: ClownData, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clown_data: ClownData = clown_data

    async def on_ready(self):
        """"Ready event handler"""
        logger.info(
            f"Logged in as `{self.user}` with ID `{self.user.id}`. Running ClownBot...")

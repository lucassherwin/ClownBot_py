"""Main entry point for ClownBot"""

import asyncio
import json
from pathlib import Path

import discord

from clown_bot.bot import ClownBot, ClownData
from clown_bot.commands.clowns import ClownInfo
from clown_bot.commands.general import General
from clown_bot.commands.wordle import Wordle
from clown_bot.config import Config

# ruff: noqa: ASYNC101


async def main():
    """Main entry point for ClownBot"""
    config = Config()

    # a client is an object that represents a connection to DIscord
    # handles events, tracks state, and interacts with Discord APIs
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    name_cache_file = Path().cwd() / config.name_cache_file

    if not name_cache_file.exists():
        name_cache_file.touch()
        name_cache = {}
    else:
        with open(name_cache_file, encoding="utf-8") as json_file:
            name_cache = json.load(json_file)

    clown_data = ClownData(name_cache=name_cache)
    bot = ClownBot(clown_data, command_prefix=config.prefix, intents=intents)

    async with bot:
        await bot.add_cog(ClownInfo(bot))
        await bot.add_cog(General(bot))
        await bot.add_cog(Wordle(bot))
        await bot.start(config.discord_token.get_secret_value())


if __name__ == "__main__":
    asyncio.run(main())

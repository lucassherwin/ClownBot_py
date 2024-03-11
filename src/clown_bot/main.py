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


async def main():
    """Main entry point for ClownBot"""
    config = Config()

    # a client is an object that represents a connection to DIscord
    # handles events, tracks state, and interacts with Discord APIs
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    file_directory = Path(__file__).parent.resolve()
    clown_file = str(file_directory / "clowns.json")
    name_cache_file = str(file_directory / "name_cache.json")

    # open the clowns.json file and read in the data
    with open(clown_file, "r", encoding="utf-8") as json_file:
        leaderboard = json.load(json_file)

    with open(name_cache_file, "r", encoding="utf-8") as json_file:
        name_cache = json.load(json_file)

    clown_data = ClownData(clown_file,
                           name_cache_file,
                           leaderboard=leaderboard,
                           name_cache=name_cache)
    bot = ClownBot(clown_data, command_prefix=config.prefix, intents=intents)

    async with bot:
        await bot.add_cog(ClownInfo(bot))
        await bot.add_cog(General(bot))
        await bot.add_cog(Wordle(bot))
        await bot.start(config.discord_token.get_secret_value())


if __name__ == "__main__":
    asyncio.run(main())

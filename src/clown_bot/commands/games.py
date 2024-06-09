"""Game commands"""

import logging
import random

from discord.ext.commands import Cog, Context, command

from clown_bot.bot import ClownBot
from clown_bot.db import add_games, get_games, remove_games

logger = logging.getLogger("ClownBot")


class Games(Cog):
    """
    Commands for managing game selection
    """

    help_text = """```
    Usage: !games <subcommand> [args]

    If adding/removing a game title with spaces, wrap the title in quotes, like `!games add "Among Us"`.

    list: List all games
    add: Add a list of games
    \t- Example: !games add "Among Us" Minecraft
    remove: Remove a list of games
    \t- Example: !games remove "Among Us"
    choose: Choose a random game
    ```"""

    def __init__(self, bot: ClownBot):
        self.bot = bot

    @command()
    async def games(self, ctx: Context, subcommand: str, *args):
        """Base command for games commands. Call `!games help` for more info.

        :param ctx: Discord Context object
        :param subcommand: Subcommand to run
        :param args: Arguments for the subcommand
        """
        if not subcommand or subcommand == "help":
            lines = [line.strip(" ") for line in self.help_text.split("\n")]
            await ctx.reply("\n".join(lines))
        elif subcommand == "list":
            await self._list_games(ctx)
        elif subcommand == "add":
            await self._add_games(ctx, args)
        elif subcommand == "remove":
            await self._remove_games(ctx, args)
        elif subcommand == "choose":
            await self._choose_game(ctx)
        else:
            await ctx.reply(f"Unknown command: {subcommand}")

    async def _list_games(self, ctx: Context):
        """
        List all games
        :param ctx: Discord Context object
        """
        games = get_games(self.bot.db, str(ctx.guild.id))
        if not games:
            await ctx.reply("No games added yet!")
            return
        await ctx.reply(f"All game options:\n{self._format_list(games)}")

    async def _add_games(self, ctx: Context, games: list[str]):
        """
        Add a game
        :param ctx: Discord Context object
        :param game: The game to add
        """
        add_games(self.bot.db, str(ctx.guild.id), games)
        await ctx.reply(f"Added games:\n{self._format_list(games)}")

    async def _remove_games(self, ctx: Context, games: list[str]):
        """
        Remove a game
        :param ctx: Discord Context object
        :param game: The game to remove
        """
        remove_games(self.bot.db, str(ctx.guild.id), games)
        await ctx.reply(f"Removed games:\n{self._format_list(games)}")

    async def _choose_game(self, ctx: Context):
        """
        Choose a random game from the list
        :param ctx: Discord Context object
        """
        games = get_games(self.bot.db, str(ctx.guild.id))
        if not games:
            await ctx.reply("No games added yet!")
            return
        game = random.choice(games)
        await ctx.reply(game)

    def _format_list(self, games: list[str]) -> str:
        return "\n".join([f"- {game}" for game in sorted(games)])

# ClownBot_py
Track who are the biggest clowns in your server!

## Commands:
* !test
  * This is a test command to make sure the bot is working
* !clowns
  * This command displays the current leaderboard of the biggest clowns
* !gamer
  * This command tells you who is a gamer
* !clownset
  * command to manually set a users clownscore
* !games - Base command for game selection functionality
  * `list` - list all games in the list of possibilities
  * `add` - add games to the list of possible games
  * `remove` - remove games from the list
  * `choose` - choose a random game from the list

## Development
You must have [Hatch](https://hatch.pypa.io/) and `make` installed. To get started initially, create a `.env` file in the top level of this repo with `DISCORD_TOKEN=<token>` in it, then run:
```bash
make start
```

Run unit tests with `make test`.

If you update the core dependency list in `pyproject.toml`, run 
```bash
hatch dep show requirements > requirements.txt
```
to export them to a requirements file. This is required for SparkedHost, where we host the bot.

Also make sure to run `make format` before merging to main to format and lint your code. This uses Hatch's built in `fmt` [command](https://hatch.pypa.io/latest/config/internal/static-analysis/)

Also ensure that you version bump appropriately with new changes. This can be done with the [hatch versioning tool](https://hatch.pypa.io/latest/version/)

### Logging
ClownBot uses the `ClownBot` logger. Log level for this can be controlled by setting the `LOG_LEVEL` env var. See [logging levels](https://docs.python.org/3/library/logging.html#logging-levels) for possible log level strings. When running locally, you can set this in your `.env` file.

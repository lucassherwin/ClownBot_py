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


## Development
You must have [Poetry](https://python-poetry.org/) and `make` installed. To get started initially, created a `.env` file in the top level of this repo with `DISCORD_TOKEN=<token>` in it, then run:
```bash
poetry env use python
make dependencies
make env
make start
```

If you update dependencies, run `make dependencies` to re-generate the `poetry.lock` file and `requirements.txt` from it. `requirements.txt` is required for SparkedHost, where we host the bot.

Also make sure to run `make format` and `make lint` before merging to main to format and lint your code, respectively.

### Logging
ClownBot uses the `ClownBot` logger. Log level for this can be controlled by setting the `LOGLEVEL` env var. See [logging levels](https://docs.python.org/3/library/logging.html#logging-levels) for possible log level strings. When running locally, you can set this in your `.env` file.

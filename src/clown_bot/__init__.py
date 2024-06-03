import logging

from clown_bot.config import Config

logger = logging.getLogger("ClownBot")
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(Config().log_level.upper())

VERSION = "0.2.0"

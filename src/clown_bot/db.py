import logging
from dataclasses import dataclass

from pydantic import NonNegativeInt
from pymongo import DESCENDING, MongoClient
from pymongo.database import Database

from clown_bot.config import Config

logger = logging.getLogger("ClownBot")


@dataclass
class Clown:
    id: int
    count: NonNegativeInt


def get_database(config: Config | None = None):
    config = config or Config()
    client = MongoClient(config.db_connection_str.get_secret_value())
    return client["clowns"]


def increment_clown(
    db: Database,
    guild_id: str,
    user_id: int,
):
    param = {"$inc": {"clown_count": 1}}
    res = db[guild_id].update_one({"_id": user_id}, param, upsert=True)
    logger.debug(f"Incremented clown result: {res}")
    return res


def set_clown(
    db: Database,
    guild_id: str,
    user_id: int,
    count: NonNegativeInt,
):
    param = {"$set": {"clown_count": count}}
    res = db[guild_id].update_one({"_id": user_id}, param, upsert=True)
    logger.debug(f"Set clown count for {user_id} to {count}")
    return res


def get_clowns(db: Database, guild_id: int, limit: int = 10) -> list[Clown]:
    clowns = db[guild_id].find().sort("clown_count", DESCENDING).limit(limit)
    clown_list = [Clown(id=clown["_id"], count=clown["clown_count"]) for clown in clowns]
    logger.debug(f"Retrieved clowns: {clown_list}")
    return clown_list

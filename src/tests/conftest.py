import pytest

from clown_bot.config import Config
from clown_bot.db import get_database


@pytest.fixture(scope="session")
def test_conf():
    return Config(
        discord_token="test_token",
        db_connection_str="mongodb://admin:password@localhost:27017",
    )


@pytest.fixture(autouse=True)
def mock_db(test_conf):
    db = get_database(test_conf)
    yield db
    for coll in db.list_collection_names():
        db.drop_collection(coll)


@pytest.fixture
def guild_id():
    return "123456"


@pytest.fixture
def user_id():
    return 56789

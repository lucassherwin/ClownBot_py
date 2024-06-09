from pymongo.database import Database

from clown_bot.db import (
    add_games,
    get_clowns,
    get_games,
    increment_clown,
    remove_games,
    set_clown,
)


def test_db_name(mock_db: Database):
    assert mock_db.name == "clowns"


def test_increment_clown(mock_db: Database, guild_id, user_id):
    increment_clown(mock_db, guild_id, user_id)
    user = mock_db[guild_id].find_one({"_id": user_id})
    assert user["clown_count"] == 1

    increment_clown(mock_db, guild_id, user_id)
    user = mock_db[guild_id].find_one({"_id": user_id})
    assert user["clown_count"] == 2


def test_set_clown(mock_db: Database, guild_id, user_id):
    num = 5
    set_clown(mock_db, guild_id, user_id, num)
    user = mock_db[guild_id].find_one({"_id": user_id})
    assert user["clown_count"] == num


def test_get_clowns(mock_db: Database, guild_id):
    num = 5
    for i in range(1, num + 1):
        set_clown(mock_db, guild_id, i, i)
    clowns = get_clowns(mock_db, guild_id)
    assert len(clowns) == num
    for i, clown in enumerate(clowns):
        assert clown.id == num - i
        assert clown.count == num - i


def test_get_clowns_limit(mock_db: Database, guild_id):
    num = 20
    limit = 10
    for i in range(1, num + 1):
        set_clown(mock_db, guild_id, i, i)
    clowns = get_clowns(mock_db, guild_id, limit)
    assert len(clowns) == limit
    for i, clown in enumerate(clowns):
        assert clown.id == num - i
        assert clown.count == num - i


def test_get_clowns_none_in_guild(mock_db: Database):
    clowns = get_clowns(mock_db, "guild_dne")
    assert clowns == []


def test_add_games(mock_db: Database, guild_id):
    game = "Amogus"
    add_games(mock_db, guild_id, game)
    db_games = get_games(mock_db, guild_id)
    assert db_games == [game]

    game2 = "Minecraft"
    add_games(mock_db, guild_id, game2)
    db_games = get_games(mock_db, guild_id)
    assert db_games == [game, game2]


def test_add_games_multiple(mock_db: Database, guild_id):
    games = ["Amogus", "Minecraft", "Among Us"]
    add_games(mock_db, guild_id, games)
    db_games = get_games(mock_db, guild_id)
    assert db_games == games


def test_add_games_duplicate(mock_db: Database, guild_id):
    game = "Amogus"
    add_games(mock_db, guild_id, game)
    db_games = get_games(mock_db, guild_id)
    assert db_games == [game]

    add_games(mock_db, guild_id, game)
    db_games = get_games(mock_db, guild_id)
    assert db_games == [game]


def test_remove_game(mock_db: Database, guild_id):
    game = "Amogus"
    add_games(mock_db, guild_id, game)
    db_games = get_games(mock_db, guild_id)
    assert db_games == [game]

    remove_games(mock_db, guild_id, game)
    db_games = get_games(mock_db, guild_id)
    assert db_games == []

    game2 = "Minecraft"
    add_games(mock_db, guild_id, game)
    add_games(mock_db, guild_id, game2)
    db_games = get_games(mock_db, guild_id)
    assert db_games == [game, game2]

    remove_games(mock_db, guild_id, game)
    db_games = get_games(mock_db, guild_id)
    assert db_games == [game2]


def test_remove_games_multiple(mock_db: Database, guild_id):
    games = ["Amogus", "Minecraft", "Among Us"]
    add_games(mock_db, guild_id, games)
    db_games = get_games(mock_db, guild_id)
    assert db_games == games

    remove_games(mock_db, guild_id, games[:2])
    db_games = get_games(mock_db, guild_id)
    assert db_games == ["Among Us"]


def test_get_games(mock_db: Database, guild_id):
    db_games = get_games(mock_db, guild_id)
    assert db_games == []

    game = "Amogus"
    add_games(mock_db, guild_id, game)
    db_games = get_games(mock_db, guild_id)
    assert db_games == [game]

    game2 = "Minecraft"
    add_games(mock_db, guild_id, game2)
    db_games = get_games(mock_db, guild_id)
    assert db_games == [game, game2]

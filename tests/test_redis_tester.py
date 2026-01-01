import fakeredis

from redis_tester import AitRedisTester


def test_crud_with_fakeredis():
    # Arrange: in-memory fake Redis with strings
    fake = fakeredis.FakeRedis(decode_responses=True)
    tester = AitRedisTester(redis_client=fake)

    # Act/Assert: connect should succeed (pings injected client)
    assert tester.connect() is True

    # Insert
    doc = {"hello": "world"}
    assert tester.insert("MY_KEY", doc) is True

    # Search
    got = tester.search("MY_KEY")
    assert got == doc

    # Update
    new_doc = {"hello": "redis"}
    assert tester.update("MY_KEY", new_doc) is True
    got2 = tester.search("MY_KEY")
    assert got2 == new_doc

    # Delete
    assert tester.delete("MY_KEY") is True
    assert tester.search("MY_KEY") is None


def test_delete_nonexistent_key_returns_false():
    fake = fakeredis.FakeRedis(decode_responses=True)
    tester = AitRedisTester(redis_client=fake)
    assert tester.connect() is True
    assert tester.delete("NOPE") is False

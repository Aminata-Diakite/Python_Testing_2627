import pytest

import server


@pytest.fixture(autouse=True)
def reset_data():
    server.clubs = server.loadClubs()
    server.competitions = server.loadCompetitions()


@pytest.fixture
def client():
    server.app.config["TESTING"] = True
    with server.app.test_client() as client:
        yield client

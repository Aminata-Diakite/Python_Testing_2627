import pytest


@pytest.fixture
def club_simply_lift():
    return {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}


@pytest.fixture
def club_iron_temple():
    return {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"}


@pytest.fixture
def competition_a_venir():
    return {"name": "Spring Festival", "date": "2999-03-27 10:00:00", "numberOfPlaces": "25"}


@pytest.fixture
def competition_passee():
    return {"name": "Old Cup", "date": "2020-01-01 10:00:00", "numberOfPlaces": "10"}

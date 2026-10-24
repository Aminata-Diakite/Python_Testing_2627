import server


def book(client, club, competition, places):
    return client.post(
        "/purchasePlaces",
        data={"club": club, "competition": competition, "places": str(places)},
    )


def find_club(name):
    return [c for c in server.clubs if c["name"] == name][0]


def find_competition(name):
    return [c for c in server.competitions if c["name"] == name][0]


def test_booking_reduces_competition_places(client):
    response = book(client, "Simply Lift", "Spring Festival", 3)
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert int(find_competition("Spring Festival")["numberOfPlaces"]) == 22


def test_booking_deducts_points_from_club(client):
    response = book(client, "Simply Lift", "Spring Festival", 3)
    assert int(find_club("Simply Lift")["points"]) == 10
    assert b"Points available: 10" in response.data

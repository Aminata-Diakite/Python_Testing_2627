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


def test_booking_more_places_than_club_points_is_refused(client):
    response = book(client, "Iron Temple", "Spring Festival", 5)
    assert b"not enough points" in response.data
    assert int(find_club("Iron Temple")["points"]) == 4
    assert int(find_competition("Spring Festival")["numberOfPlaces"]) == 25


def test_booking_exactly_all_club_points_is_accepted(client):
    response = book(client, "Iron Temple", "Spring Festival", 4)
    assert b"Great-booking complete!" in response.data
    assert int(find_club("Iron Temple")["points"]) == 0


def test_booking_more_than_12_places_in_one_request_is_refused(client):
    response = book(client, "Simply Lift", "Spring Festival", 13)
    assert b"more than 12" in response.data
    assert int(find_club("Simply Lift")["points"]) == 13
    assert int(find_competition("Spring Festival")["numberOfPlaces"]) == 25


def test_booking_exactly_12_places_is_accepted(client):
    response = book(client, "Simply Lift", "Spring Festival", 12)
    assert b"Great-booking complete!" in response.data
    assert int(find_club("Simply Lift")["points"]) == 1


def test_booking_cumulative_places_above_12_is_refused(client):
    book(client, "Simply Lift", "Spring Festival", 8)
    response = book(client, "Simply Lift", "Spring Festival", 6)
    assert b"more than 12" in response.data
    assert int(find_club("Simply Lift")["points"]) == 5
    assert int(find_competition("Spring Festival")["numberOfPlaces"]) == 17

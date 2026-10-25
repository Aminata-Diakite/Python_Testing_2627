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
    book(client, "Simply Lift", "Spring Festival", 4)
    response = book(client, "Simply Lift", "Spring Festival", 9)
    assert b"more than 12" in response.data
    assert int(find_club("Simply Lift")["points"]) == 9
    assert int(find_competition("Spring Festival")["numberOfPlaces"]) == 21

def test_booking_more_places_than_available_is_refused(client):
    server.competitions.append(
        {"name": "Mini Cup", "date": "2027-06-01 10:00:00", "numberOfPlaces": "2"}
    )
    response = book(client, "Simply Lift", "Mini Cup", 3)
    assert b"not enough places" in response.data
    assert int(find_competition("Mini Cup")["numberOfPlaces"]) == 2
    assert int(find_club("Simply Lift")["points"]) == 13


PAST_COMPETITION = {
    "name": "Old Cup",
    "date": "2020-01-01 10:00:00",
    "numberOfPlaces": "10",
}


def test_booking_past_competition_is_refused(client):
    server.competitions.append(dict(PAST_COMPETITION))
    response = book(client, "Simply Lift", "Old Cup", 2)
    assert b"already taken place" in response.data
    assert int(find_competition("Old Cup")["numberOfPlaces"]) == 10
    assert int(find_club("Simply Lift")["points"]) == 13


def test_welcome_page_hides_booking_link_for_past_competition(client):
    server.competitions.append(dict(PAST_COMPETITION))
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert b"/book/Old%20Cup/" not in response.data
    assert b"/book/Spring%20Festival/" in response.data


def test_booking_zero_places_is_refused(client):
    response = book(client, "Simply Lift", "Spring Festival", 0)
    assert b"valid number" in response.data
    assert int(find_club("Simply Lift")["points"]) == 13


def test_booking_negative_places_is_refused(client):
    response = book(client, "Simply Lift", "Spring Festival", -3)
    assert b"valid number" in response.data
    assert int(find_club("Simply Lift")["points"]) == 13
    assert int(find_competition("Spring Festival")["numberOfPlaces"]) == 25


def test_booking_text_instead_of_number_is_refused(client):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "abc"},
    )
    assert response.status_code == 200
    assert b"valid number" in response.data


def test_booking_empty_places_is_refused(client):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": ""},
    )
    assert response.status_code == 200
    assert b"valid number" in response.data

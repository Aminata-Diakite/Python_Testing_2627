def test_points_board_is_public_and_lists_all_clubs(client):
    response = client.get("/points")
    assert response.status_code == 200
    assert b"Simply Lift" in response.data
    assert b"Iron Temple" in response.data
    assert b"She Lifts" in response.data


def test_points_board_shows_each_club_points(client):
    response = client.get("/points")
    assert b"13" in response.data
    assert b"4" in response.data
    assert b"12" in response.data


def test_points_board_reflects_points_after_booking(client):
    client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "3"},
    )
    response = client.get("/points")
    assert b"<td>10</td>" in response.data


def test_points_board_has_a_link_back_to_login(client):
    response = client.get("/points")
    assert b'href="/"' in response.data


def test_login_page_links_to_points_board(client):
    response = client.get("/")
    assert b'href="/points"' in response.data

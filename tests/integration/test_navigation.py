def test_book_page_for_known_club_and_competition_shows_form(client):
    response = client.get("/book/Spring Festival/Simply Lift")
    assert response.status_code == 200
    assert b"Spring Festival" in response.data
    assert b'name="places"' in response.data


def test_logout_redirects_to_login_page(client):
    response = client.get("/logout")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

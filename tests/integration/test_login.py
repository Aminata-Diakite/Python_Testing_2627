def test_login_with_known_email_shows_summary(client):
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert response.status_code == 200
    assert b"Welcome, john@simplylift.co" in response.data


def test_login_with_unknown_email_shows_error_and_does_not_crash(client):
    response = client.post("/showSummary", data={"email": "inconnu@nowhere.com"})
    assert response.status_code == 200
    assert b"Unknown email" in response.data

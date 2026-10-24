import server


def test_load_clubs_returns_the_three_clubs():
    clubs = server.loadClubs()
    assert len(clubs) == 3
    assert clubs[0]["name"] == "Simply Lift"

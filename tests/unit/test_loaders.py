import server


def test_chargement_des_clubs_retourne_les_trois_clubs():
    clubs = server.loadClubs()
    assert len(clubs) == 3
    assert clubs[0]["name"] == "Simply Lift"

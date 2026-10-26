def test_tableau_des_points_est_public_et_liste_tous_les_clubs(client):
    response = client.get("/points")
    assert response.status_code == 200
    assert b"Simply Lift" in response.data
    assert b"Iron Temple" in response.data
    assert b"She Lifts" in response.data


def test_tableau_des_points_affiche_les_points_de_chaque_club(client):
    response = client.get("/points")
    assert b"13" in response.data
    assert b"4" in response.data
    assert b"12" in response.data


def test_tableau_des_points_reflete_les_points_apres_une_reservation(client):
    client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Spring Festival", "places": "3"},
    )
    response = client.get("/points")
    assert b">10</td>" in response.data


def test_tableau_des_points_contient_un_lien_vers_la_connexion(client):
    response = client.get("/points")
    assert b'href="/"' in response.data


def test_page_de_connexion_contient_un_lien_vers_le_tableau_des_points(client):
    response = client.get("/")
    assert b'href="/points"' in response.data

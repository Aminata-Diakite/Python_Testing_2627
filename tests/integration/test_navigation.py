from tests.helpers import texte


def test_page_de_reservation_pour_un_club_et_une_competition_connus(client):
    response = client.get("/book/Spring Festival/Simply Lift")
    assert response.status_code == 200
    assert "Spring Festival" in texte(response)
    assert 'name="places"' in texte(response)


def test_deconnexion_redirige_vers_la_page_de_connexion(client):
    response = client.get("/logout")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

import server
from tests.helpers import connecter


def points_de(nom):
    return int(next(c for c in server.clubs if c["name"] == nom)["points"])


def test_reservation_sans_connexion_est_refusee(client):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Iron Temple", "competition": "Spring Festival", "places": "3"},
    )
    assert response.status_code == 302
    assert points_de("Iron Temple") == 4


def test_page_de_reservation_sans_connexion_renvoie_a_la_connexion(client):
    response = client.get("/book/Spring Festival/Simply Lift")
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


def test_apres_deconnexion_la_page_de_reservation_est_fermee(client):
    connecter(client, "Simply Lift")
    client.get("/logout")
    response = client.get("/book/Spring Festival/Simply Lift")
    assert response.status_code == 302


def test_un_club_ne_peut_pas_reserver_pour_un_autre_club(client):
    connecter(client, "Simply Lift")
    response = client.post(
        "/purchasePlaces",
        data={"club": "Iron Temple", "competition": "Spring Festival", "places": "3"},
    )
    assert response.status_code == 302
    assert points_de("Iron Temple") == 4
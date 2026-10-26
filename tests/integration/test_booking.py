import server
from tests.helpers import texte


def reserver(client, club, competition, places):
    return client.post(
        "/purchasePlaces",
        data={"club": club, "competition": competition, "places": str(places)},
    )


def trouver_club(nom):
    return [c for c in server.clubs if c["name"] == nom][0]


def trouver_competition(nom):
    return [c for c in server.competitions if c["name"] == nom][0]


COMPETITION_PASSEE = {
    "name": "Old Cup",
    "date": "2020-01-01 10:00:00",
    "numberOfPlaces": "10",
}


def test_reservation_reduit_les_places_de_la_competition(client):
    response = reserver(client, "Simply Lift", "Spring Festival", 3)
    assert response.status_code == 200
    assert "Réservation effectuée avec succès" in texte(response)
    assert int(trouver_competition("Spring Festival")["numberOfPlaces"]) == 22


def test_reservation_deduit_les_points_du_club(client):
    response = reserver(client, "Simply Lift", "Spring Festival", 3)
    assert int(trouver_club("Simply Lift")["points"]) == 10
    assert "Points disponibles : 10" in texte(response)


def test_reservation_au_dela_des_points_du_club_est_refusee(client):
    response = reserver(client, "Iron Temple", "Spring Festival", 5)
    assert "pas assez de points" in texte(response)
    assert int(trouver_club("Iron Temple")["points"]) == 4
    assert int(trouver_competition("Spring Festival")["numberOfPlaces"]) == 25


def test_reservation_avec_exactement_tous_les_points_est_acceptee(client):
    response = reserver(client, "Iron Temple", "Spring Festival", 4)
    assert "Réservation effectuée avec succès" in texte(response)
    assert int(trouver_club("Iron Temple")["points"]) == 0


def test_reservation_de_plus_de_12_places_en_une_demande_est_refusee(client):
    response = reserver(client, "Simply Lift", "Spring Festival", 13)
    assert "plus de 12 places" in texte(response)
    assert int(trouver_club("Simply Lift")["points"]) == 13
    assert int(trouver_competition("Spring Festival")["numberOfPlaces"]) == 25


def test_reservation_de_exactement_12_places_est_acceptee(client):
    response = reserver(client, "Simply Lift", "Spring Festival", 12)
    assert "Réservation effectuée avec succès" in texte(response)
    assert int(trouver_club("Simply Lift")["points"]) == 1


def test_reservations_cumulees_au_dela_de_12_places_sont_refusees(client):
    reserver(client, "Simply Lift", "Spring Festival", 4)
    response = reserver(client, "Simply Lift", "Spring Festival", 9)
    assert "plus de 12 places" in texte(response)
    assert int(trouver_club("Simply Lift")["points"]) == 9
    assert int(trouver_competition("Spring Festival")["numberOfPlaces"]) == 21


def test_reservation_de_plus_de_places_que_disponible_est_refusee(client):
    server.competitions.append(
        {"name": "Mini Cup", "date": "2027-06-01 10:00:00", "numberOfPlaces": "2"}
    )
    response = reserver(client, "Simply Lift", "Mini Cup", 3)
    assert "pas assez de places" in texte(response)
    assert int(trouver_competition("Mini Cup")["numberOfPlaces"]) == 2
    assert int(trouver_club("Simply Lift")["points"]) == 13


def test_reservation_dune_competition_passee_est_refusee(client):
    server.competitions.append(dict(COMPETITION_PASSEE))
    response = reserver(client, "Simply Lift", "Old Cup", 2)
    assert "a déjà eu lieu" in texte(response)
    assert int(trouver_competition("Old Cup")["numberOfPlaces"]) == 10
    assert int(trouver_club("Simply Lift")["points"]) == 13


def test_page_daccueil_masque_le_lien_de_reservation_des_competitions_passees(client):
    server.competitions.append(dict(COMPETITION_PASSEE))
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert b"/book/Old%20Cup/" not in response.data
    assert b"/book/Spring%20Festival/" in response.data


def test_reservation_de_zero_place_est_refusee(client):
    response = reserver(client, "Simply Lift", "Spring Festival", 0)
    assert "nombre de places valide" in texte(response)
    assert int(trouver_club("Simply Lift")["points"]) == 13


def test_reservation_dun_nombre_negatif_de_places_est_refusee(client):
    response = reserver(client, "Simply Lift", "Spring Festival", -3)
    assert "nombre de places valide" in texte(response)
    assert int(trouver_club("Simply Lift")["points"]) == 13
    assert int(trouver_competition("Spring Festival")["numberOfPlaces"]) == 25


def test_reservation_avec_du_texte_a_la_place_dun_nombre_est_refusee(client):
    response = reserver(client, "Simply Lift", "Spring Festival", "abc")
    assert response.status_code == 200
    assert "nombre de places valide" in texte(response)


def test_reservation_sans_nombre_de_places_est_refusee(client):
    response = reserver(client, "Simply Lift", "Spring Festival", "")
    assert response.status_code == 200
    assert "nombre de places valide" in texte(response)


def test_page_de_reservation_avec_une_competition_inconnue_ne_plante_pas(client):
    response = client.get("/book/Inconnue/Simply Lift")
    assert response.status_code == 200
    assert "Une erreur est survenue" in texte(response)


def test_page_de_reservation_avec_un_club_inconnu_ne_plante_pas(client):
    response = client.get("/book/Spring Festival/Inconnu")
    assert response.status_code == 200
    assert "Une erreur est survenue" in texte(response)


def test_achat_avec_une_competition_inconnue_ne_plante_pas(client):
    response = reserver(client, "Simply Lift", "Inconnue", 1)
    assert response.status_code == 200
    assert "Une erreur est survenue" in texte(response)


def test_achat_avec_un_club_inconnu_ne_plante_pas(client):
    response = reserver(client, "Inconnu", "Spring Festival", 1)
    assert response.status_code == 200
    assert "Une erreur est survenue" in texte(response)

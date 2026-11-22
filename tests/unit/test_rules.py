import server


def test_is_past_vrai_pour_une_competition_passee(competition_passee):
    resultat = server.is_past(competition_passee)

    assert resultat is True


def test_is_past_faux_pour_une_competition_a_venir(competition_a_venir):
    resultat = server.is_past(competition_a_venir)

    assert resultat is False


def test_parse_places_accepte_un_entier_positif():
    saisie = "3"

    resultat = server.parse_places(saisie)

    assert resultat == 3


def test_parse_places_refuse_zero():
    saisie = "0"

    resultat = server.parse_places(saisie)

    assert resultat == 0


def test_parse_places_refuse_un_nombre_negatif():
    saisie = "-2"

    resultat = server.parse_places(saisie)

    assert resultat == 0


def test_parse_places_refuse_du_texte():
    saisie = "abc"

    resultat = server.parse_places(saisie)

    assert resultat == 0


def test_parse_places_refuse_une_chaine_vide():
    saisie = ""

    resultat = server.parse_places(saisie)

    assert resultat == 0


def test_parse_places_refuse_none():
    saisie = None

    resultat = server.parse_places(saisie)

    assert resultat == 0


def test_check_booking_reservation_valide(club_simply_lift, competition_a_venir):
    points = int(club_simply_lift["points"])
    places_dispo = int(competition_a_venir["numberOfPlaces"])

    message = server.check_booking(3, points=points, available=places_dispo, already=0)

    assert message is None


def test_check_booking_points_insuffisants(club_iron_temple, competition_a_venir):
    points = int(club_iron_temple["points"])
    places_dispo = int(competition_a_venir["numberOfPlaces"])

    message = server.check_booking(5, points=points, available=places_dispo, already=0)

    assert "points" in message


def test_check_booking_places_insuffisantes(club_simply_lift, competition_a_venir):
    competition_a_venir["numberOfPlaces"] = "2"
    points = int(club_simply_lift["points"])
    places_dispo = int(competition_a_venir["numberOfPlaces"])

    message = server.check_booking(3, points=points, available=places_dispo, already=0)

    assert "places disponibles" in message


def test_check_booking_limite_depassee_en_une_demande(club_simply_lift, competition_a_venir):
    points = int(club_simply_lift["points"])
    places_dispo = int(competition_a_venir["numberOfPlaces"])

    message = server.check_booking(13, points=points, available=places_dispo, already=0)

    assert "12" in message


def test_check_booking_limite_depassee_en_cumulant(club_simply_lift, competition_a_venir):
    points = int(club_simply_lift["points"])
    places_dispo = int(competition_a_venir["numberOfPlaces"])

    message = server.check_booking(9, points=points, available=places_dispo, already=4)

    assert "12" in message


def test_check_booking_exactement_12_places_est_accepte(club_simply_lift, competition_a_venir):
    points = int(club_simply_lift["points"])
    places_dispo = int(competition_a_venir["numberOfPlaces"])

    message = server.check_booking(12, points=points, available=places_dispo, already=0)

    assert message is None


def test_check_booking_tous_les_points_sont_acceptes(club_iron_temple, competition_a_venir):
    points = int(club_iron_temple["points"])
    places_dispo = int(competition_a_venir["numberOfPlaces"])

    message = server.check_booking(4, points=points, available=places_dispo, already=0)

    assert message is None

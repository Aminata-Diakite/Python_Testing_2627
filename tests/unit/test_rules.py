import server


def test_is_past_vrai_pour_une_date_ancienne():
    assert server.is_past({"date": "2020-01-01 10:00:00"}) is True


def test_is_past_faux_pour_une_date_future():
    assert server.is_past({"date": "2999-01-01 10:00:00"}) is False


def test_parse_places_accepte_un_entier_positif():
    assert server.parse_places("3") == 3


def test_parse_places_refuse_zero():
    assert server.parse_places("0") == 0


def test_parse_places_refuse_un_nombre_negatif():
    assert server.parse_places("-2") == 0


def test_parse_places_refuse_du_texte():
    assert server.parse_places("abc") == 0


def test_parse_places_refuse_une_chaine_vide():
    assert server.parse_places("") == 0


def test_parse_places_refuse_none():
    assert server.parse_places(None) == 0


def test_check_booking_reservation_valide():
    assert server.check_booking(3, points=13, available=25, already=0) is None


def test_check_booking_points_insuffisants():
    assert "points" in server.check_booking(5, points=4, available=25, already=0)


def test_check_booking_places_insuffisantes():
    message = server.check_booking(3, points=13, available=2, already=0)
    assert "places disponibles" in message


def test_check_booking_limite_depassee_en_une_demande():
    assert "12" in server.check_booking(13, points=20, available=25, already=0)


def test_check_booking_limite_depassee_en_cumulant_les_reservations():
    assert "12" in server.check_booking(9, points=20, available=25, already=4)


def test_check_booking_exactement_12_places_est_accepte():
    assert server.check_booking(12, points=13, available=25, already=0) is None


def test_check_booking_tous_les_points_sont_acceptes():
    assert server.check_booking(4, points=4, available=25, already=0) is None


def test_chargement_des_competitions_retourne_des_noms():
    competitions = server.loadCompetitions()
    assert all("name" in c for c in competitions)

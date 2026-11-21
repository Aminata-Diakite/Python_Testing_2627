import server


# ---------- is_past : la compétition est-elle passée ? ----------

def test_is_past_vrai_pour_une_competition_passee(competition_passee):
    # Arrange : la fixture fournit une compétition datée de 2020
    # Act
    resultat = server.is_past(competition_passee)
    # Assert
    assert resultat is True


def test_is_past_faux_pour_une_competition_a_venir(competition_a_venir):
    # Arrange : la fixture fournit une compétition datée de 2999
    # Act
    resultat = server.is_past(competition_a_venir)
    # Assert
    assert resultat is False


# ---------- parse_places : lire le nombre de places tapé ----------

def test_parse_places_accepte_un_entier_positif():
    # Arrange
    saisie = "3"
    # Act
    resultat = server.parse_places(saisie)
    # Assert
    assert resultat == 3


def test_parse_places_refuse_zero():
    # Arrange
    saisie = "0"
    # Act
    resultat = server.parse_places(saisie)
    # Assert : 0 veut dire « saisie refusée »
    assert resultat == 0


def test_parse_places_refuse_un_nombre_negatif():
    # Arrange
    saisie = "-2"
    # Act
    resultat = server.parse_places(saisie)
    # Assert
    assert resultat == 0


def test_parse_places_refuse_du_texte():
    # Arrange
    saisie = "abc"
    # Act
    resultat = server.parse_places(saisie)
    # Assert
    assert resultat == 0


def test_parse_places_refuse_une_chaine_vide():
    # Arrange
    saisie = ""
    # Act
    resultat = server.parse_places(saisie)
    # Assert
    assert resultat == 0


def test_parse_places_refuse_none():
    # Arrange : le champ est absent du formulaire
    saisie = None
    # Act
    resultat = server.parse_places(saisie)
    # Assert
    assert resultat == 0


# ---------- check_booking : vérifier une réservation ----------

def test_check_booking_reservation_valide(club_simply_lift, competition_a_venir):
    # Arrange : Simply Lift a 13 points, la compétition a 25 places
    points = int(club_simply_lift["points"])
    places_dispo = int(competition_a_venir["numberOfPlaces"])
    # Act
    message = server.check_booking(3, points=points, available=places_dispo, already=0)
    # Assert : None veut dire « réservation acceptée »
    assert message is None


def test_check_booking_points_insuffisants(club_iron_temple, competition_a_venir):
    # Arrange : Iron Temple n'a que 4 points
    points = int(club_iron_temple["points"])
    places_dispo = int(competition_a_venir["numberOfPlaces"])
    # Act : il demande 5 places
    message = server.check_booking(5, points=points, available=places_dispo, already=0)
    # Assert
    assert "points" in message


def test_check_booking_places_insuffisantes(club_simply_lift, competition_a_venir):
    # Arrange : il ne reste que 2 places dans la compétition
    competition_a_venir["numberOfPlaces"] = "2"
    points = int(club_simply_lift["points"])
    places_dispo = int(competition_a_venir["numberOfPlaces"])
    # Act : le club en demande 3
    message = server.check_booking(3, points=points, available=places_dispo, already=0)
    # Assert
    assert "places disponibles" in message


def test_check_booking_limite_depassee_en_une_demande(club_simply_lift, competition_a_venir):
    # Arrange
    points = int(club_simply_lift["points"])
    places_dispo = int(competition_a_venir["numberOfPlaces"])
    # Act : 13 places d'un coup
    message = server.check_booking(13, points=points, available=places_dispo, already=0)
    # Assert
    assert "12" in message


def test_check_booking_limite_depassee_en_cumulant(club_simply_lift, competition_a_venir):
    # Arrange : le club a déjà réservé 4 places
    points = int(club_simply_lift["points"])
    places_dispo = int(competition_a_venir["numberOfPlaces"])
    # Act : il en demande 9 de plus (4 + 9 = 13)
    message = server.check_booking(9, points=points, available=places_dispo, already=4)
    # Assert
    assert "12" in message


def test_check_booking_exactement_12_places_est_accepte(club_simply_lift, competition_a_venir):
    # Arrange
    points = int(club_simply_lift["points"])
    places_dispo = int(competition_a_venir["numberOfPlaces"])
    # Act : pile la limite
    message = server.check_booking(12, points=points, available=places_dispo, already=0)
    # Assert
    assert message is None


def test_check_booking_tous_les_points_sont_acceptes(club_iron_temple, competition_a_venir):
    # Arrange : Iron Temple a 4 points
    points = int(club_iron_temple["points"])
    places_dispo = int(competition_a_venir["numberOfPlaces"])
    # Act : il réserve 4 places
    message = server.check_booking(4, points=points, available=places_dispo, already=0)
    # Assert
    assert message is None


# ---------- chargement des données ----------

def test_chargement_des_competitions_retourne_des_noms():
    # Act
    competitions = server.loadCompetitions()
    # Assert
    assert all("name" in c for c in competitions)

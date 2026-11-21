from datetime import datetime
from unittest.mock import MagicMock, mock_open, patch

import server


# ---------- Mock de l'horloge : is_past dépend de la date du jour ----------

def test_is_past_vrai_quand_on_avance_la_date_du_jour(competition_a_venir):
    # Arrange : une fausse horloge, bloquée en l'an 3000
    horloge = MagicMock(wraps=datetime)
    horloge.now.return_value = datetime(3000, 1, 1)
    # Act
    with patch("server.datetime", horloge):
        resultat = server.is_past(competition_a_venir)
    # Assert : en 3000, la compétition de 2999 est passée
    assert resultat is True
    horloge.now.assert_called_once()


def test_is_past_faux_a_la_minute_exacte_de_la_competition(competition_a_venir):
    # Arrange : l'horloge est bloquée pile à l'heure de la compétition
    horloge = MagicMock(wraps=datetime)
    horloge.now.return_value = datetime(2999, 3, 27, 10, 0, 0)
    # Act
    with patch("server.datetime", horloge):
        resultat = server.is_past(competition_a_venir)
    # Assert : la compétition commence, elle n'est pas encore passée
    assert resultat is False


def test_is_past_vrai_une_seconde_apres_le_debut(competition_a_venir):
    # Arrange : l'horloge est bloquée une seconde après le début
    horloge = MagicMock(wraps=datetime)
    horloge.now.return_value = datetime(2999, 3, 27, 10, 0, 1)
    # Act
    with patch("server.datetime", horloge):
        resultat = server.is_past(competition_a_venir)
    # Assert
    assert resultat is True


# ---------- Mock des fichiers : ne pas dépendre de clubs.json ----------

def test_load_clubs_lit_le_fichier_clubs_json():
    # Arrange : un faux fichier clubs.json, avec un seul club
    contenu = '{"clubs": [{"name": "Club Test", "email": "test@club.co", "points": "5"}]}'
    faux_fichier = mock_open(read_data=contenu)
    # Act
    with patch("builtins.open", faux_fichier):
        clubs = server.loadClubs()
    # Assert : le club vient bien du faux fichier
    assert clubs[0]["name"] == "Club Test"
    faux_fichier.assert_called_once_with('clubs.json')


def test_load_competitions_lit_le_fichier_competitions_json():
    # Arrange : un faux fichier competitions.json
    contenu = '{"competitions": [{"name": "Cup Test", "date": "2999-01-01 10:00:00", ' \
              '"numberOfPlaces": "8"}]}'
    faux_fichier = mock_open(read_data=contenu)
    # Act
    with patch("builtins.open", faux_fichier):
        competitions = server.loadCompetitions()
    # Assert
    assert competitions[0]["name"] == "Cup Test"
    faux_fichier.assert_called_once_with('competitions.json')


def test_load_clubs_appelle_json_load_une_seule_fois():
    # Arrange : on remplace json.load par un mock qui renvoie une liste vide
    faux_json = MagicMock(return_value={"clubs": []})
    # Act
    with patch("builtins.open", mock_open()), patch("server.json.load", faux_json):
        clubs = server.loadClubs()
    # Assert : la liste vient du mock, et json.load a été appelé une fois
    assert clubs == []
    faux_json.assert_called_once()

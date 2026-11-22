from datetime import datetime
from unittest.mock import MagicMock, mock_open, patch

import server


def test_is_past_vrai_quand_on_avance_la_date_du_jour(competition_a_venir):
    horloge = MagicMock(wraps=datetime)
    horloge.now.return_value = datetime(3000, 1, 1)

    with patch("server.datetime", horloge):
        resultat = server.is_past(competition_a_venir)

    assert resultat is True
    horloge.now.assert_called_once()


def test_is_past_faux_a_la_minute_exacte_de_la_competition(competition_a_venir):
    horloge = MagicMock(wraps=datetime)
    horloge.now.return_value = datetime(2999, 3, 27, 10, 0, 0)

    with patch("server.datetime", horloge):
        resultat = server.is_past(competition_a_venir)

    assert resultat is False


def test_is_past_vrai_une_seconde_apres_le_debut(competition_a_venir):
    horloge = MagicMock(wraps=datetime)
    horloge.now.return_value = datetime(2999, 3, 27, 10, 0, 1)

    with patch("server.datetime", horloge):
        resultat = server.is_past(competition_a_venir)

    assert resultat is True


def test_load_clubs_lit_le_fichier_clubs_json():
    contenu = '{"clubs": [{"name": "Club Test", "email": "test@club.co", "points": "5"}]}'
    faux_fichier = mock_open(read_data=contenu)

    with patch("builtins.open", faux_fichier):
        clubs = server.loadClubs()

    assert clubs[0]["name"] == "Club Test"
    faux_fichier.assert_called_once_with('clubs.json')


def test_load_competitions_lit_le_fichier_competitions_json():
    contenu = '{"competitions": [{"name": "Cup Test", "date": "2999-01-01 10:00:00", ' \
              '"numberOfPlaces": "8"}]}'
    faux_fichier = mock_open(read_data=contenu)

    with patch("builtins.open", faux_fichier):
        competitions = server.loadCompetitions()

    assert competitions[0]["name"] == "Cup Test"
    faux_fichier.assert_called_once_with('competitions.json')


def test_load_clubs_appelle_json_load_une_seule_fois():
    faux_json = MagicMock(return_value={"clubs": []})

    with patch("builtins.open", mock_open()), patch("server.json.load", faux_json):
        clubs = server.loadClubs()

    assert clubs == []
    faux_json.assert_called_once()

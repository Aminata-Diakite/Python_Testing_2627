from tests.helpers import texte


def test_connexion_avec_un_email_connu_affiche_le_resume(client):
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert response.status_code == 200
    assert "Bienvenue, john@simplylift.co" in texte(response)


def test_connexion_avec_un_email_inconnu_affiche_une_erreur_sans_planter(client):
    response = client.post("/showSummary", data={"email": "inconnu@nowhere.com"})
    assert response.status_code == 200
    assert "Adresse e-mail inconnue" in texte(response)

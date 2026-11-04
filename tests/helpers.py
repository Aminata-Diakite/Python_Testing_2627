import html


def texte(reponse):
    return html.unescape(reponse.get_data(as_text=True))


def connecter(client, nom_club):
    import server
    club = next((c for c in server.clubs if c["name"] == nom_club), None)
    if club:
        client.post("/showSummary", data={"email": club["email"]})
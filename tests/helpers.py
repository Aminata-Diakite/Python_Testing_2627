import html


def texte(reponse):
    return html.unescape(reponse.get_data(as_text=True))

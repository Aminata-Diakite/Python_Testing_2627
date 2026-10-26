import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
MAX_PLACES_PER_COMPETITION = 12
bookings = {}


def is_past(competition):
    date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
    return date < datetime.now()


app.jinja_env.globals['is_past'] = is_past


def parse_places(raw):
    try:
        value = int(raw)
    except (ValueError, TypeError):
        return 0
    return value if value > 0 else 0


def check_booking(places, points, available, already):
    if places > available:
        return "Erreur : il n'y a pas assez de places disponibles dans cette compétition."
    if places > points:
        return "Erreur : vous n'avez pas assez de points pour réserver ce nombre de places."
    if already + places > MAX_PLACES_PER_COMPETITION:
        return (f"Erreur : vous ne pouvez pas réserver plus de "
                f"{MAX_PLACES_PER_COMPETITION} places dans une compétition.")
    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    matching_clubs = [club for club in clubs if club['email'] == request.form['email']]
    if not matching_clubs:
        flash("Adresse e-mail inconnue, veuillez réessayer.", "erreur")
        return render_template('index.html')
    return render_template('welcome.html', club=matching_clubs[0], competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    flash("Une erreur est survenue, veuillez réessayer.", "erreur")
    return render_template('index.html')


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)
    if competition is None or club is None:
        flash("Une erreur est survenue, veuillez réessayer.", "erreur")
        return render_template('index.html')
    placesRequired = parse_places(request.form.get('places'))
    if placesRequired == 0:
        flash("Erreur : veuillez saisir un nombre de places valide.", "erreur")
        return render_template('welcome.html', club=club, competitions=competitions)
    if is_past(competition):
        flash("Erreur : cette compétition a déjà eu lieu.", "erreur")
        return render_template('welcome.html', club=club, competitions=competitions)
    already = bookings.get((club['name'], competition['name']), 0)
    error = check_booking(placesRequired, int(club['points']),
                          int(competition['numberOfPlaces']), already)
    if error:
        flash(error, "erreur")
        return render_template('welcome.html', club=club, competitions=competitions)
    bookings[(club['name'], competition['name'])] = already + placesRequired
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    club['points'] = int(club['points'])-placesRequired
    flash("Réservation effectuée avec succès !", "succes")
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/points')
def points():
    return render_template('points.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

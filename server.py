import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for


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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    matching_clubs = [club for club in clubs if club['email'] == request.form['email']]
    if not matching_clubs:
        flash("Unknown email, please try again.")
        return render_template('index.html')
    return render_template('welcome.html', club=matching_clubs[0], competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    flash("Something went wrong-please try again")
    return render_template('index.html')


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)
    if competition is None or club is None:
        flash("Something went wrong-please try again")
        return render_template('index.html')
    try:
        placesRequired = int(request.form['places'])
    except ValueError:
        placesRequired = 0
    if placesRequired <= 0:
        flash("Error: please enter a valid number of places.")
        return render_template('welcome.html', club=club, competitions=competitions)
    if is_past(competition):
        flash("Error: this competition has already taken place.")
        return render_template('welcome.html', club=club, competitions=competitions)
    if placesRequired > int(competition['numberOfPlaces']):
        flash("Error: not enough places available in this competition.")
        return render_template('welcome.html', club=club, competitions=competitions)
    if placesRequired > int(club['points']):
        flash("Error: not enough points to book this number of places.")
        return render_template('welcome.html', club=club, competitions=competitions)
    already = bookings.get((club['name'], competition['name']), 0)
    if already + placesRequired > MAX_PLACES_PER_COMPETITION:
        flash("Error: you cannot book more than 12 places in a competition.")
        return render_template('welcome.html', club=club, competitions=competitions)
    bookings[(club['name'], competition['name'])] = already + placesRequired
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    club['points'] = int(club['points'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)

# TODO: Add route for points display

@app.route('/logout')
def logout():
    return redirect(url_for('index'))
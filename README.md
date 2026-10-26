# GUDLFT, réservation de places pour les compétitions

Application Flask permettant aux secrétaires de clubs d'échanger leurs points contre des places de compétition. Les données sont dans `clubs.json` et `competitions.json` (pas de base de données, tout est remis à zéro au redémarrage).

## Règles métier (Spécifications fonctionnelles)

- 1 point = 1 place ; un club ne peut pas réserver plus de places qu'il n'a de points
- maximum 12 places par club et par compétition (cumul compris)
- impossible de réserver plus que les places restantes, ni une compétition passée
- tableau public des points : `/points` (sans connexion)

## Installation

Python 3.10 ou plus est nécessaire (testé avec 3.12 et 3.13). Remplacer `<url du dépôt>` par l'adresse du dépôt GitHub.

### macOS ou Linux (Terminal)

    git clone <url du dépôt>
    cd Python_Testing_2627
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    flask --app server run --port 5001

Ouvrir http://127.0.0.1:5001. Le port 5001 est volontaire : sur macOS, le port 5000 est souvent occupé par le service AirPlay (erreur « Address already in use » ou page « 403 »). Si Python 3 n'est pas installé : `brew install python` (Homebrew) ou l'installeur de python.org.

### Windows (PowerShell)

    git clone <url du dépôt>
    cd Python_Testing_2627
    py -3.12 -m venv env
    env\Scripts\activate
    pip install -r requirements.txt
    flask --app server run

Ouvrir http://127.0.0.1:5000.

### Utilisation

E-mails de test : `john@simplylift.co`, `admin@irontemple.com`, `kate@shelifts.co.uk`. Le style utilise le CDN Tailwind : une connexion internet est nécessaire pour l'affichage. Pour quitter l'environnement virtuel : `deactivate`.

## Tests

    pytest
    pytest --cov=server
    flake8 server.py tests --max-line-length=100

Dossiers : `tests/unit`, `tests/integration`, `tests/performance`.

Test de charge (serveur lancé dans un autre terminal ; sur macOS remplacer le port 5000 par 5001) :

    locust -f tests/performance/locustfile.py --host http://127.0.0.1:5000 --users 6 --spawn-rate 2 --run-time 30s --headless

## Conventions

- Branches : `bug/nom-descriptif`, `fonctionnalite/nom-descriptif`, `amelioration/nom-descriptif`, une par sujet
- Commits : un par unité de travail, préfixés `test:`, `fix:`, `feat:`, `style:`, `refactor:`, `perf:`, `chore:`, `docs:`
- TDD : le commit `test:` précède le commit `fix:` ou `feat:`
- `main` ne reçoit que du code dont les tests passent ; la branche `qa` n'est jamais fusionnée

## Rapports

Branche `qa` : `docs/rapport-tests.md`, `docs/rapport-performance.md` et `reports/` (couverture HTML, tests, Locust).

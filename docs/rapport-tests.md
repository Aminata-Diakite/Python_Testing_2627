# Rapport de tests, GUDLFT (phases 1 et 2)

## Résultats

| Indicateur | Résultat | Objectif du guide |
|---|---|---|
| Tests exécutés | 82, tous réussis | tous verts avant fusion dans `main` |
| Couverture de `server.py` | 100 % (83 instructions, 0 manquante) | au moins 60 % |
| flake8 (`--max-line-length=100`) | 0 erreur | code propre |
| Tests unitaires | 55 | deux fois plus que les autres |
| Tests d'intégration | 27 | |

Commande : `pytest tests/unit tests/integration --cov=server --cov-report=html:reports/coverage --html=reports/tests.html --self-contained-html`

Au départ, flake8 relevait 24 erreurs de style dans le `server.py` d'origine (espaces, indentation, lignes vides). Elles ont été corrigées dans les commits `style:`.

## Organisation

- `tests/unit` : fonctions pures (`parse_places`, `check_booking`, `is_past`, chargement des JSON). Les cas limites sont paramétrés, donc une ligne de code peut produire plusieurs tests.
- `tests/integration` : routes Flask avec le client de test (connexion, réservation, tableau des points, navigation).
- `tests/performance` : scénario Locust, voir `rapport-performance.md`.
- Les données sont rechargées avant chaque test (fixture `reset_data`), donc les tests sont indépendants.

## Bogues corrigés (un test écrit avant chaque correctif)

| Branche | Bogue | Cas testés (chemin normal / chemin d'erreur) |
|---|---|---|
| `bug/email-inconnu` | `IndexError` si l'e-mail n'existe pas | e-mail connu / inconnu |
| `bug/dates-competitions` | dates de 2020, aucune réservation possible | (données) |
| `bug/deduction-points` | points du club jamais déduits | réservation de 3 places, 13 points deviennent 10 |
| `bug/points-insuffisants` | réservation au-delà des points | 5 places avec 4 points refusées / 4 places acceptées |
| `bug/limite-12-places` | limite de 12 absente, cumul compris | 13 refusées / 12 acceptées / 4 puis 9 refusées |
| `bug/places-disponibles` | places négatives | 3 places demandées sur 2 disponibles refusées |
| `bug/competition-passee` | compétition passée réservable | réservation refusée, lien masqué |
| `bug/saisie-places-invalide` | saisie vide, nulle, négative ou texte | 0, -3, "abc", vide refusés |
| `bug/reservation-introuvable` | `IndexError` sur club ou compétition inconnu | 4 combinaisons inconnues |

Fonctionnalité de la phase 2 : `fonctionnalite/tableau-points-public` (page `/points`, publique, en lecture seule).

## Limites connues

- Le style Tailwind (CDN) n'est pas couvert par les tests : il a été vérifié à l'œil.
- Les données vivent en mémoire : un redémarrage du serveur remet tout à zéro (voulu par la spécification).

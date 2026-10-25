# Rapport de performance, GUDLFT

## Conditions du test

- Outil : Locust 2.47.0, scénario `tests/performance/locustfile.py`
- 6 utilisateurs (valeur par défaut du guide), montée de 2 par seconde, durée 30 s
- Serveur de développement Flask en local (`127.0.0.1:5000`), Python 3.12.10, Windows
- Données : `competitions.json` et `clubs.json` d'origine

Commande : `locust -f tests/performance/locustfile.py --host http://127.0.0.1:5000 --users 6 --spawn-rate 2 --run-time 30s --headless --html reports/performance.html --csv reports/performance`

## Résultats (fichier `reports/performance_stats.csv`)

| Route | Requêtes | Échecs | Médiane | Moyenne | Max | 95e centile | Seuil |
|---|---|---|---|---|---|---|---|
| POST `/showSummary` (liste des compétitions) | 74 | 0 | 8 ms | 11,2 ms | 59,8 ms | 20 ms | 5 s |
| POST `/purchasePlaces` (mise à jour des points) | 19 | 0 | 10 ms | 11,3 ms | 20,6 ms | 21 ms | 2 s |
| GET `/points` (tableau public) | 22 | 0 | 7 ms | 8,3 ms | 17,9 ms | 18 ms | n/a |
| Total | 115 | 0 | 8 ms | 10,7 ms | 59,8 ms | 20 ms | |

Débit moyen : 3,95 requêtes par seconde.

## Conclusion

- Chargement de la liste des compétitions : maximum 59,8 ms pour un seuil de 5 s. Conforme.
- Mise à jour des points : maximum 20,6 ms pour un seuil de 2 s. Conforme.
- Aucune requête n'a échoué.

## Réserves

- Charge faible (6 utilisateurs) sur une machine locale : ces chiffres valident le seuil du guide, pas la capacité d'un déploiement réel.
- Le club « She Lifts » n'a que 12 points : une fois la limite atteinte, les réservations suivantes sont refusées par la règle métier (réponse HTTP 200 avec message d'erreur). Les temps de réponse restent valables, ce sont des réponses réelles du serveur.

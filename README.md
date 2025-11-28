# Projet ModSim (Dash multipage)

Ce projet est une application Dash multipage pour l’analyse de stabilité via la figure de Poincaré, avec:
- une navigation fiable par clic sur les zones de la figure,
- un système de logs centralisé (fichier rotatif),
- des pages dédiées pour chaque zone,
- une suite de tests automatisés (pytest + dash-duo).

La figure Poincaré a été reconstruite pour correspondre fidèlement à la référence, et les identifiants de composants ont été normalisés (sans accents) afin d’éviter les problèmes de sérialisation.

## Prérequis

- Python 3.9+
- Pip
- (Optionnel) `venv` pour isoler l’environnement

## Installation

1) Créer et activer un environnement virtuel

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Installer les dépendances

```bash
pip install -r requirements.txt
```

## Lancement de l’application

L’application est une app Dash multipage. Pour la démarrer, exécutez:

```bash
python run.py
```

Par défaut:
- une page d’accueil existe sur `/`,
- la page Poincaré est disponible sur `/poincare`,
- un sommaire de stabilité est disponible sur `/stabilite`,
- des pages de zones sont accessibles sous `/stabilite/zone-...`,
- une page `about` est disponible sur `/about`.

Navigation:
- Les clics sur la figure Poincaré déclenchent une navigation serveur vers la page d’information de la zone.
- La configuration actuelle utilise `dcc.Location(refresh=True)` pour garantir une mise à jour fiable de l’interface après chaque changement d’URL (rechargement complet).

## Structure (repères utiles)

- `src/app/app.py` — instanciation/paramétrage de l’app Dash et `dcc.Location(refresh=True)`
- `src/app/logging_setup.py` — initialisation du logging (fichier rotatif `logs/app.log`)
- `src/app/poincare/figure.py` — construction de la figure Poincaré (traces, styles, ordre)
- `src/app/poincare/callbacks.py` — callbacks de la figure (hover/click) et navigation serveur
- `src/app/pages/` — pages multipage:
  - `home.py` — page d’accueil (`/`)
  - `poincare.py` — page Poincaré (`/poincare`)
  - `stabilite_summary.py` — sommaire (`/stabilite`)
  - `stabilite/zone_*.py` — pages des zones
  - `about.py` — page À propos (`/about`)
- `logs/app.log` — fichier de logs (rotatif)

## Journaux (logging)

Un mécanisme de logging centralisé est en place:
- Écriture dans `logs/app.log` avec rotation (taille et nombre de fichiers limités).
- Console configurée au niveau WARNING pour réduire le bruit.
- Utilitaires disponibles (`init_logging()`, `get_logger()`, `reconfigure_logging()`).

Consultez `logs/app.log` pour diagnostiquer les événements, la navigation, et les callbacks.

## Tests

La suite de tests utilise `pytest` et, pour les tests de l’UI Dash, `dash[testing]` (`dash-duo`).

Installation recommandée pour les tests UI:
```bash
pip install "dash[testing]"
```

Lancement des tests:
```bash
pytest
```

Contenu de la suite:
- Vérification de la structure et de l’ordre des traces de la figure Poincaré.
- Import de l’app et validation basique du multipage.
- Navigation directe vers les pages (par URL).
- Test tolérant de la navigation par clic (flaky selon l’environnement); vous pouvez préférer des tests unitaires qui simulent `clickData` côté Python.

Conseils:
- Lancez `pytest` depuis la racine du projet.
- Si un test de clic DOM est instable, remplacez-le par un test qui injecte un `clickData` simulé dans le callback Python.

## Dépannage

- La navigation ne rafraîchit pas la page cible:
  - La configuration actuelle force le rafraîchissement avec `refresh=True`. Si vous changez à `refresh=False`, assurez-vous que l’ordre d’instanciation de l’app et l’enregistrement des pages est correct, et évitez le reloader qui double-initialise.
- Les clics sur la figure ne semblent rien faire:
  - Vérifiez que la figure conserve l’ordre des traces attendu par les callbacks.
  - Contrôlez les logs dans `logs/app.log`.
- Problèmes liés aux caractères accentués dans les IDs:
  - Les IDs ont été normalisés (sans accents). Ne réintroduisez pas d’accents dans les IDs des composants.

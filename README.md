# Projet ModSim (Dash multipage)

Application Dash multipage pour explorer la stabilité de systèmes linéaires d’ordre 2 via le diagramme de Poincaré. Navigation serveur fiable (clic sur zones), design system centralisé, logging rotatif et pages dédiées pour chaque type d’équilibre.

📄 Documentation clé : `ARCHITECTURE.md` (vue complète), `DEPLOYMENT.md` (mise en ligne), `CLEANUP_REPORT.md` (nettoyage & docstrings).

## Prérequis

- Python 3.9+
- pip
- (optionnel) venv pour isoler l’environnement

## Installation

1) Créer et activer un environnement virtuel

```bash
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

2) Installer les dépendances

```bash
pip install -r requirements.txt
```

## Lancement

```bash
python run.py
```

Pages disponibles :

- `/` accueil
- `/poincare` diagramme Poincaré
- `/stabilite` sommaire stabilité
- `/stabilite/<type>` foyers, nœuds, selle, centre, lignes de PE, mouvement uniforme
- `/about` à propos
- `/chaos` page expérimentale (chaos solaire avec slider de conditions initiales)

## Structure rapide

- `src/app/app.py` : création Dash, layout principal, sidebar
- `src/app/logging_setup.py` : logging rotatif `logs/app.log`
- `src/app/poincare/` : figure, layout, callbacks, zones, constantes
- `src/app/stabilite/` : base_layout, base_figures, eigenvalue_utils, callbacks, 11 types d’équilibres
- `src/app/pages/` : pages multipage (`home`, `poincare`, `main_stabilite_page`, `about`, pages `/stabilite/*`)
- `src/app/style/` : design system (palette, typography, components)
- `logs/app.log` : logs rotatifs

## Logging

- Fichier rotatif `logs/app.log` (1MB, 5 backups)
- Console en WARNING pour limiter le bruit
- Utilitaires : `init_logging()`, `get_logger()`, `reconfigure_logging()`

## Tests

```bash
# (optionnel) tests UI
pip install "dash[testing]"

# lancer la suite
pytest
```

Couverture : structure/ordre des traces Poincaré, import app & navigation multipage, navigation directe, clic simulé (clickData) côté Python.

## Dépannage rapide

- Navigation : `dcc.Location(refresh=True)` déjà activé; si `refresh=False`, soigner l’ordre d’instanciation.
- Clics inactifs : vérifier l’ordre des traces attendu par les callbacks et consulter `logs/app.log`.
- IDs : normalisés sans accents (ne pas en réintroduire).

## Pour aller plus loin

- Architecture détaillée : `ARCHITECTURE.md`
- Guide de mise en ligne : `DEPLOYMENT.md`
- Rapport de nettoyage/docstrings : `CLEANUP_REPORT.md`

# Architecture du Projet ModSim

## Vue d'ensemble

Projet-ModSim est une application Dash multipage pour l'analyse interactive de la stabilité des systèmes linéaires du second ordre via le diagramme de Poincaré.

### Stack technique
- **Framework:** Dash (Python web framework)
- **Visualisation:** Plotly (graphiques interactifs)
- **Calculs:** NumPy, SciPy (algèbre linéaire, EDO)
- **Logging:** Python `logging` (custom rotating file handler)

---

## Structure des répertoires

```
src/
├── __init__.py                    # Exports lazy pour create_app/get_app
├── app/
│   ├── __init__.py               # Re-exports de poincare et app
│   ├── app.py                    # Instance Dash, configuration, layouts multipage
│   ├── logging_setup.py          # System de logging centralisé (INFO→file, WARNING→console)
│   ├── analyzer/                 # Utilitaires de calcul (System, StabilityAnalyzer, Plot)
│   ├── poincare/                 # Module Poincaré
│   │   ├── __init__.py           # Exports (figure, layout, callbacks, zones)
│   │   ├── figure.py             # Construction de la figure Poincaré (traces, zones)
│   │   ├── layout.py             # Layout HTML du diagramme
│   │   ├── callbacks.py          # Callbacks (hover/click) et navigation
│   │   ├── constants.py          # Paramètres (TAU_MIN, TAU_MAX, N_SAMPLES)
│   │   ├── zones.py              # Mapping zones → pages (navigation)
│   │   └── __pycache__/
│   ├── stabilite/                # Module d'analyse de stabilité
│   │   ├── base_layout.py        # Template layout pour toutes les pages stabilité
│   │   ├── base_figures.py       # Générateurs de diagramme de phase
│   │   ├── base_callbacks.py     # Template callbacks pour affichage eigenvalues/ODE
│   │   ├── eigenvalue_utils.py   # Calcul eigenvalues, classification équilibre
│   │   ├── *.py                  # 11 fichiers d'équilibre (foyer_stable, noeud_*, etc.)
│   │   │                         # Chaque définit: layout_pedagogic(), register_callbacks()
│   │   └── main_stabilite_page.py # Page résumé /stabilite
│   ├── pages/                    # Pages multipage Dash
│   │   ├── home.py               # Page d'accueil (/)
│   │   ├── poincare.py           # Page du diagramme Poincaré (/poincare)
│   │   ├── main_stabilite_page.py # Résumé des équilibres (/stabilite)
│   │   ├── about.py              # À propos (/about)
│   │   └── stabilite/            # Pages des 11 types d'équilibre
│   │       ├── foyer_stable.py, foyer_instable.py, ...
│   │       └── (enregistre routes /stabilite/*, construit layouts via base_layout)
│   └── style/                    # Design system centralisé
│       ├── palette.py            # Couleurs (warm orange theme)
│       ├── typography.py         # Fonts, sizes
│       ├── theme.py              # Dataclasses style (Palette, Typography)
│       ├── components/
│       │   ├── layout.py         # Fonctions de style (app_container, nav_button, etc.)
│       │   └── sidebar.py        # Style du menu latéral
│       └── plot/
│           └── theme.py          # Styles Plotly (couleurs traces, zones)
│
├── __init__.py                   # Exports du package src
├── pages/
└── __pycache__/

logs/
└── app.log                       # Logs rotatifs (1MB max, 5 backups)

tests/
├── conftest.py                   # Fixtures pytest/dash-duo
└── *.py                          # Suites tests (figure, navigation, pages)

requirements.txt                  # Dépendances Python
run.py                           # Point d'entrée (python run.py)
README.md                        # Guide d'utilisation
ARCHITECTURE.md                  # Ce fichier
```

---

## Flux de données

### 1. Démarrage de l'application

```
run.py → create_app() → Dash instance
  │
  ├→ [Auto-discovery des pages] → @dash.register_page() dans src/app/pages/**/*.py
  │
  ├→ Poincaré figure (cached) → build_poincare_figure() → PoincareConfig
  │
  ├→ Sidebar + Layout principal (HTML) → dcc.Location() pour navigation
  │
  └→ register_callbacks() pour tous les modules
```

### 2. Navigation par clic sur Poincaré

```
User clicks zone on diagram
  │
  ├→ clickData callback → determine zone (meta label)
  │
  ├→ Find corresponding page from zones.py mapping
  │
  └→ dcc.Location(pathname) → Server-side refresh → Load new page
```

### 3. Affichage d'une page d'équilibre

```
URL: /stabilite/foyer_stable
  │
  ├→ Dash auto-loads src/app/pages/stabilite/foyer_stable.py
  │
  ├→ build_stability_layout("foyer_stable", layout_pedagogic, τ, Δ)
  │
  ├→ Callbacks listen to element IDs (ph-foyer-stable-{graph,phase,ode,...})
  │
  ├→ Formulate matrix from (τ, Δ) → eigenvalue_utils.tau_delta_to_matrix()
  │
  ├→ Calculate eigenvalues → classify equilibrium
  │
  └→ Render: pedagogic text + graph + eigenvalue info + phase diagram
```

---

## Système de styling

### Architecture

Tous les styles sont centralisés dans `src/app/style/`:

```
style/
├── palette.py          # Couleurs (PALETTE dataclass)
├── typography.py       # Fonts (TYPOGRAPHY dataclass)
├── components/
│   ├── layout.py       # Fonctions de style pour containers/cards/buttons
│   └── sidebar.py      # Style du menu latéral
└── plot/
    └── theme.py        # Thème Plotly pour figures
```

### Principe: Single Source of Truth

- **Une seule couleur primaire** (#EA580C orange warm)
- **Une seule palette** importée partout
- **Fonctions de style réutilisables** (app_container, nav_button, section_card, etc.)

### Exemple d'utilisation

```python
from src.app.style.components.layout import app_container, content_wrapper

html.Div(
    [
        html.H1("Title"),
        html.P("Content"),
    ],
    style={
        **app_container(),        # Background, text color, min-height
        **content_wrapper(),      # Sidebar offset, padding
    }
)
```

---

## Logging

### Configuration

Défini dans `src/app/logging_setup.py`:

```python
LoggingConfig(
    file_path="logs/app.log",
    file_level=logging.INFO,
    console_level=logging.WARNING,
    max_bytes=1_000_000,           # Rotation tous les 1MB
    backup_count=5,                # Garde 5 versions
)
```

### Usage

```python
from src.app.logging_setup import get_logger

log = get_logger(__name__)
log.info("Application started")
log.debug("Detailed diagnostic info")
log.warning("Something unexpected")
```

---

## Pages et routes

### Pages principales

| Route | Fichier | Description |
|-------|---------|-------------|
| `/` | `pages/home.py` | Page d'accueil |
| `/poincare` | `pages/poincare.py` | Diagramme interactif |
| `/stabilite` | `pages/main_stabilite_page.py` | Résumé des équilibres |
| `/about` | `pages/about.py` | Documentation/À propos |

### Pages d'équilibre (11 types)

```
/stabilite/foyer_stable
/stabilite/foyer_instable
/stabilite/noeud_stable
/stabilite/noeud_instable
/stabilite/noeud_stable_degenere
/stabilite/noeud_instable_degenere
/stabilite/selle
/stabilite/centre
/stabilite/ligne_pe_stable
/stabilite/ligne_pe_instable
/stabilite/mouvement_uniforme
```

Chacune est générée via `src/app/stabilite/` + template `base_layout.py`.

---

## Modules clés

### `poincare/figure.py`

Construit la figure Poincaré avec:
- **Parabole noire** (τ² = 4Δ) séparant régions stables/instables
- **11 zones colorées** correspondant aux 11 types d'équilibre
- **Traces Plotly** avec indices 0..10 pour callbacks

### `stabilite/eigenvalue_utils.py`

Convertit (τ, Δ) → eigenvalues → classification:

```
Poincaré plane (τ, Δ)
    ↓
tau_delta_to_matrix() → Matrix coefficients [a b; c d]
    ↓
calculate_eigenvalues() → λ₁, λ₂ (real/complex)
    ↓
classify_equilibrium() → Type d'équilibre + nature
```

### `stabilite/base_figures.py`

Génère les diagrammes de phase:
- **Trajectoires** (solve ODE avec scipy.integrate.odeint)
- **Champ de vecteurs** (arrows direction field)
- **Points d'équilibre** (marqueurs)
- **Séparatrices** (pour selles)

### `poincare/callbacks.py`

Gère les interactions utilisateur:
- **Hover** → Surligner zone
- **Click** → Navigate to `/stabilite/{type}`
- **Zone mapping** → Meta labels → Page names

---

## Flux d'une analyse

1. **Utilisateur arrive** sur `/`
2. **Clique sur le diagramme Poincaré** dans une zone (ex: "Foyer stable")
3. **Callback capture** le clic + détermine zone
4. **Navigation** vers `/stabilite/foyer_stable`
5. **Page charge** et affiche:
   - Explication pédagogique
   - Valeurs propres calculées
   - Équation différentielle
   - Diagramme de phase avec trajectoires
6. **Utilisateur explore** puis clique "Retour" ou "Autre zone"

---

## Performance et Optimisation

### Caching

- **Figure Poincaré**: Construite une fois au démarrage et réutilisée
- **Phase diagrams**: Générées à la demande (peu coûteux)

### Logging

- **File rotation**: Évite croissance infinie des logs
- **Levels**: INFO→file, WARNING→console (bruit réduit)

### Dash

- `suppress_callback_exceptions=True` pour multipage
- `refresh=True` pour fiabilité navigation

---

## Extensibilité

### Ajouter un nouveau type d'équilibre

1. Créer `src/app/stabilite/nouveau_type.py`:
   ```python
   PAGE_KEY = "nouveau_type"
   
   def layout_pedagogic() -> html.Div:
       return html.Div([...])
   
   def register_callbacks(app) -> None:
       register_stability_callbacks(app, PAGE_KEY, tau=..., delta=...)
   ```

2. Créer `src/app/pages/stabilite/nouveau_type.py`:
   ```python
   import dash
   from src.app.stabilite.nouveau_type import layout_pedagogic
   
   dash.register_page(__name__, path="/stabilite/nouveau_type", ...)
   layout = build_stability_layout("nouveau_type", layout_pedagogic, ...)
   ```

3. Ajouter zone à `poincare/zones.py` et figure Poincaré

---

## Nettoyage et Maintenance

### Structure épurée
- ✅ Pas de fichiers temporaires (`src/temp/` supprimé)
- ✅ Imports non-utilisés supprimés
- ✅ Docstrings complètes sur modules clés
- ✅ Fichiers d'__init__.py propres avec __all__

### Qualité du code
- Noms clairs et constants importants en MAJUSCULES
- Fonctions courtes avec docstrings + type hints
- Modules spécialisés (analyse, présentation, style)
- Logging strategic aux points importants


from __future__ import annotations

import dash
from dash import html  # type: ignore

from src.app.poincare.callbacks import register_callbacks
from src.app.poincare.figure import get_cached_poincare_figure
from src.app.poincare.layout import build_layout

# Enregistrement de la page (native multipage)
dash.register_page(
    __name__,
    path="/poincare",
    name="Poincaré",
    title="Diagramme de Poincaré",
    description="Visualisation des zones de stabilité locales pour systèmes linéaires d'ordre 2.",
    order=0,
)

# Construction / récupération de la figure immuable via cache
_base_figure = get_cached_poincare_figure()

# Layout principal réutilisant la fonction existante
# (contient déjà le Graph + zones + panneaux de sortie)
_layout_core = build_layout(_base_figure)

# Possibilité d’envelopper pour ajouter des éléments spécifiques à la page
layout = html.Div(
    [
        _layout_core,
        html.Div(
            [
                html.Small(
                    "Page Poincaré – multipage natif Dash. Ajoutez d'autres pages dans src/app/pages/.",
                    style={"color": "#555"},
                )
            ],
            style={"marginTop": "12px"},
        ),
    ],
    style={"padding": "8px"},
)
# Attacher les callbacks spécifiques à cette page (hover / click sur la figure)
# Utilise l'instance Dash active récupérée via dash.get_app()
try:
    register_callbacks(dash.get_app(), _base_figure)
except Exception:
    # Si dash.get_app() n'est pas disponible (versions anciennes), ignorer silencieusement
    pass


def get_figure():
    """
    Retourne la figure immuable (utilitaire si besoin externe).
    """
    return _base_figure

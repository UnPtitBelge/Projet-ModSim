"""
Page multipage native Dash : Diagramme de Poincaré.

Cette page :
- enregistre sa route ("/")
- construit la figure (parabole + zones)
- expose un layout avec les IDs attendus par les callbacks:
    "poincare-graph", "output-temp-hover", "output-temp-click"

Les callbacks ne sont pas définis ici : ils sont attachés via
`register_callbacks` dans le module principal ou dans le module callbacks.

Cette page utilise un cache interne pour éviter de recalculer la figure à chaque import.
"""

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


# ---------------------------------------------------------------------------
# OPTIONNEL : Listener de route pour le debug
# ---------------------------------------------------------------------------
# Ce callback (à activer si nécessaire) permet d’afficher la route courante
# et de vérifier que le changement de pathname (dcc.Location) est bien propagé.
# Par défaut il est commenté pour ne pas surcharger l’interface.
#
# Pour l’activer :
#   1. Décommenter le décorateur et la fonction ci-dessous.
#   2. Ajouter un composant html.Div(id="debug-route") dans le layout si on
#      préfère ne pas réutiliser un ID existant.
#
# Exemple d’usage : valider que la navigation clientside déclenche bien le
# rerender multipage sans nécessiter de refresh manuel.
#
# @dash.get_app().callback(Output("output-temp-hover", "children"),
#                          Input("url", "pathname"),
#                          prevent_initial_call=True)
# def _debug_current_path(pathname: str):
#     return f"Route active: {pathname}"
# ---------------------------------------------------------------------------

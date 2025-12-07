from __future__ import annotations
from typing import Optional

import plotly.graph_objects as go
from dash import Input, Output, html

from src.app.stabilite.base_layout import build_stability_layout, stability_ids

# Clé de page pour "Centre"
PAGE_KEY = "foyer_stable"

__all__ = [
    "PAGE_KEY",
    "get_ids",
    "build_layout",
    "register_callbacks",
]


def get_ids() -> dict[str, str]:
    """
    Retourne les IDs normalisés des placeholders pour la page Centre.
    - graph: ID du graphique interactif
    - phase: ID du diagramme de phase
    - explication: ID du bloc d'explication pédagogique
    """
    return stability_ids(PAGE_KEY)


def build_layout() -> html.Div:
    """
    Construit le layout minimal pour la page Centre:
    - Graphique interactif (dcc.Graph)
    - Diagramme de phase (dcc.Graph)
    - Explication pédagogique (html.Div)
    """
    return build_stability_layout(PAGE_KEY)


def register_callbacks(app) -> None:
    """
    Enregistre les callbacks personnalisés pour la page Foyer stable.
    """
    ids = stability_ids(PAGE_KEY)

    # Explication pédagogique personnalisée
    @app.callback(
        Output(ids["explication"], "children"),
        Input(ids["explication"], "id"),
        prevent_initial_call=False,
    )
    def _update_explication(_explication_id: Optional[str]):
        return [
            html.P(
                "Un foyer stable est un point d'équilibre où les trajectoires convergent en suivant des spirales vers celui-ci. "
                " Nous pouvons en déduire que le système est asymptotiquement stable. "
            ),
            html.H4("Exemple de la vie réelle :"),
            html.Ul(
                [
                    html.Li(
                        "Le poids suspendu à un ressort suspendu: Lorsqu'on déplace le poids de sa position d'équilibre et qu'on le relâche, il oscille de haut en bas avant de revenir à sa position d'équilibre stable."
                    ),
                    html.Li(
                        "Le pendule: Un pendule qui oscille dans l'air perd de l'énergie à cause des frottements, ce qui le fait revenir à sa position d'équilibre stable."
                    ),
                ]
            ),
            html.H4("Caractéristiques mathématiques:"),
            html.Ul(
                [
                    html.Li("$\\tau$ > 0"),
                    html.Li("$\\Delta$ > $\\tau^2/4$"),
                    html.Li("Racines complexes"),
                    html.Li("Partie réelle négative"),
                    html.Li("Comportement: stable oscillatoire amorti"),
                ]
            ),
        ]

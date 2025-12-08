from __future__ import annotations
from typing import Optional

import plotly.graph_objects as go
from dash import Input, Output, html

from src.app.stabilite.base_callbacks import register_stability_callbacks
from src.app.stabilite.base_layout import build_stability_layout, stability_ids
from src.app.stabilite.base_figures import create_phase_diagram

# Clé de page pour "Foyer stable"
PAGE_KEY = "foyer_stable"

__all__ = [
    "PAGE_KEY",
    "get_ids",
    "register_callbacks",
    "layout_pedagogic",
]


def get_ids() -> dict[str, str]:
    """
    Retourne les IDs normalisés des placeholders pour la page Foyer stable.
    - graph: ID du graphique interactif
    - phase: ID du diagramme de phase
    - explication: ID du bloc d'explication pédagogique
    """
    return stability_ids(PAGE_KEY)


def create_figure() -> go.Figure:
    """
    Crée le diagramme de phase pour un foyer stable.
    Paramètres: a=-1, b=1, c=-1, d=-1
    """
    return create_phase_diagram(a=-1, b=1, c=-1, d=-1, title="Foyer stable")

def layout_pedagogic() -> html.Div:
    """
    Retourne le contenu pédagogique pour la page Foyer stable.
    """
    return html.Div([
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
    ])

def register_callbacks(app) -> None:
    """
    Enregistre les callbacks personnalisés pour la page Foyer stable.
    """
    register_stability_callbacks(app, PAGE_KEY, create_figure)

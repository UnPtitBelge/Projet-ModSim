from __future__ import annotations

from typing import Optional

import plotly.graph_objects as go
from dash import Input, Output, html

from src.app.stabilite.base_callbacks import register_stability_callbacks
from src.app.stabilite.base_figures import create_phase_diagram
from src.app.stabilite.base_layout import build_stability_layout, stability_ids

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


def get_constraints() -> dict:
    """
    Retourne les contraintes pour les sliders pour un foyer stable.

    Foyer stable:
    - τ < 0 (trace négative)
    - Δ > τ²/4 (racines complexes)
    - Partie réelle négative

    Returns:
        dict avec tau_min, tau_max, delta_min, delta_max, default_tau, default_delta
    """
    return {
        "tau_min": -5.0,
        "tau_max": -0.1,  # Strictement négatif
        "delta_min": 0.5,  # Pour garantir Δ > τ²/4 avec τ=-5, τ²/4=6.25
        "delta_max": 8.0,
        "default_tau": -2.0,
        "default_delta": 2.0,
    }


def layout_pedagogic() -> html.Div:
    """
    Retourne le contenu pédagogique pour la page Foyer stable.
    """
    return html.Div(
        [
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
                    html.Li("$\\tau < 0$ (trace négative)"),
                    html.Li("$\\Delta > \\tau^2/4$ (racines complexes)"),
                    html.Li("Partie réelle négative"),
                    html.Li("Comportement: stable oscillatoire amorti"),
                ]
            ),
        ]
    )


def register_callbacks(app) -> None:
    """
    Enregistre les callbacks pour la page Foyer stable.
    """
    # Foyer stable: τ < 0, Δ > τ²/4
    register_stability_callbacks(
        app, PAGE_KEY, tau=-2.0, delta=2.0, create_phase_fig=create_figure
    )

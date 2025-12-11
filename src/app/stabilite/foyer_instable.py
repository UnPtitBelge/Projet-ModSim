from __future__ import annotations

from typing import Optional

import plotly.graph_objects as go
from dash import Input, Output, html  # type: ignore

from src.app.stabilite.base_callbacks import register_stability_callbacks
from src.app.stabilite.base_figures import create_phase_diagram
from src.app.stabilite.base_layout import build_stability_layout, stability_ids

# Clé de page pour "Centre"
PAGE_KEY = "foyer_instable"

__all__ = [
    "PAGE_KEY",
    "get_ids",
    "register_callbacks",
    "layout_pedagogic",
]


def get_ids() -> dict[str, str]:
    """
    Retourne les IDs normalisés des placeholders pour la page Centre.
    - graph: ID du graphique interactif
    - phase: ID du diagramme de phase
    - explication: ID du bloc d'explication pédagogique
    """
    return stability_ids(PAGE_KEY)


def create_figure() -> go.Figure:
    """
    Crée le diagramme de phase pour un foyer instable.
    Paramètres: a=1, b=1, c=-1, d=1
    """
    return create_phase_diagram(a=1, b=1, c=-1, d=1, title="Foyer instable")


def get_constraints() -> dict:
    """
    Retourne les contraintes pour les sliders pour un foyer instable.

    Foyer instable:
    - τ > 0 (trace positive)
    - Δ > τ²/4 (racines complexes)
    """
    return {
        "tau_min": 0.1,  # Strictement positif
        "tau_max": 5.0,
        "delta_min": 0.5,
        "delta_max": 8.0,
        "default_tau": 2.0,
        "default_delta": 2.0,
    }


def layout_pedagogic() -> html.Div:
    """
    Retourne le contenu pédagogique pour la page Foyer instable.
    """
    return html.Div(
        [
            html.P(
                "Un point d’équilibre est un foyer instable lorsque les valeurs propres sont complexes conjuguées avec une partie réelle strictement positive. Les trajectoires tournent autour de l’équilibre mais s’en éloignent de plus en plus. La partie réelle positive entraîne une croissance exponentielle, ce qui rend l’équilibre instable."
            ),
            html.H4("Exemple de la vie réelle :"),
            html.Ul(
                [
                    html.Li(
                        "Le pendule inversé: Lorsqu'on place un pendule en position verticale avec le poids vers le haut, cette position est instable et lorsqu'on le perturbe légèrement, il bascule et s'éloigne de cette position d'équilibre instable."
                    ),
                    html.Li(
                        "Le larsen acoustique: Est un équilibre instable quand un microphone capte le son d'un haut-parleur et que celui-ci est trop proche mais que le son n'est pas assez fort pour perturber l'équilibre. Cependant, dès qu'une petite perturbation augmente le volume, le son devient de plus en plus fort, s'éloignant ainsi de l'état initial instable."
                    ),
                ]
            ),
            html.H4("Caractéristiques mathématiques:"),
            html.Ul(
                [
                    html.Li("$\\tau$ < 0"),
                    html.Li("$\\Delta$ > $\\tau^2/4$"),
                    html.Li("Racines complexes"),
                    html.Li("Partie réelle positive"),
                    html.Li("Comportement: instable oscillatoire"),
                ]
            ),
        ]
    )


def register_callbacks(app) -> None:
    """
    Enregistre les callbacks pour la page Foyer instable.
    """
    # Foyer instable: τ > 0, Δ > τ²/4
    register_stability_callbacks(
        app, PAGE_KEY, tau=2.0, delta=2.0, create_phase_fig=create_figure
    )

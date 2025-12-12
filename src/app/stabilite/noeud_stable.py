from __future__ import annotations

from typing import Optional

import plotly.graph_objects as go
from dash import Input, Output, html  # type: ignore

from src.app.stabilite.base_callbacks import register_stability_callbacks
from src.app.stabilite.base_figures import create_phase_diagram
from src.app.stabilite.base_layout import build_stability_layout, stability_ids

# Clé de page pour "Centre"
PAGE_KEY = "noeud_stable"

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
    Crée le diagramme de phase pour un nœud stable.
    Paramètres: a=-2, b=0, c=0, d=-1
    """
    return create_phase_diagram(a=-2, b=0, c=0, d=-1, title="Nœud stable")


def get_constraints() -> dict:
    """
    Retourne les contraintes pour les sliders pour un noeud stable.

    Noeud stable:
    - τ < 0 (trace négative)
    - 0 < Δ < τ²/4 (racines réelles distinctes)
    """
    return {
        "tau_min": -5.0,
        "tau_max": -0.1,  # Strictement négatif
        "delta_min": 0.1,
        "delta_max": 2.0,
        "default_tau": -3.0,
        "default_delta": 1.0,
    }


def layout_pedagogic() -> html.Div:
    """
    Retourne le contenu pédagogique pour la page Nœud stable.
    """
    return html.Div(
        [
            html.P(
                "Un point d’équilibre est un noeud stable lorsque les valeurs propres sont réelles, négatives. Les trajectoires se dirigent vers l’équilibre sans osciller, en suivant des directions privilégiées correspondant aux vecteurs propres. Comme toutes les valeurs propres sont négatives, les perturbations décroissent exponentiellement ce qui rend l’équilibre asymptotiquement stable."
            ),
            html.H4("Exemple de la vie réelle:"),
            html.Ul(
                [
                    html.Li(
                        "Une bille placée au bord d'une cuvette, qui va rouler vers le fond de celle-ci et s'y stabiliser sans oscillations lorsqu'on la perturbe légèrement, le fond de la cuvette représentant un noeud stable."
                    ),
                    html.Li(
                        "Le cruise control d'une voiture: Lorsqu'on active le cruise control, le système ajuste automatiquement la vitesse de la voiture pour maintenir la vitesse cible constante. Si la voiture ralentit légèrement, le système augmente la puissance pour revenir à la vitesse définie, et vice versa, assurant ainsi une stabilité sans oscillations autour de la vitesse choisie."
                    ),
                ]
            ),
            html.H4("Caractéristiques mathématiques:"),
            html.Ul(
                [
                    html.Li("$\\tau$ > 0"),
                    html.Li("0 < $\\Delta$ < $\\tau^2/4$"),
                    html.Li("Deux racines réelles négatives"),
                    html.Li("Stable non oscillatoire"),
                ]
            ),
        ]
    )


def register_callbacks(app) -> None:
    """
    Enregistre les callbacks pour la page Noeud stable.
    """
    # Noeud stable: τ < 0, 0 < Δ < τ²/4
    register_stability_callbacks(
        app, PAGE_KEY, tau=-3.0, delta=1.0, create_phase_fig=create_figure
    )

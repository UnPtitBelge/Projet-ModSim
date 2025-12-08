from __future__ import annotations

import plotly.graph_objects as go
from dash import html  # type: ignore

from src.app.stabilite.base_callbacks import register_stability_callbacks
from src.app.stabilite.base_figures import create_phase_diagram
from src.app.stabilite.base_layout import build_stability_layout, stability_ids

# Clé de page pour "Selle"
PAGE_KEY = "selle"

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
    Crée le diagramme de phase pour un point selle.
    Paramètres: a=1, b=1, c=1, d=-1
    """
    return create_phase_diagram(a=1, b=1, c=1, d=-1, title="Point selle")


def get_constraints() -> dict:
    """
    Retourne les contraintes pour les sliders pour une selle.

    Selle:
    - Δ < 0 (déterminant négatif)
    - τ peut être n'importe quelle valeur
    """
    return {
        "tau_min": -5.0,
        "tau_max": 5.0,
        "delta_min": -2.0,
        "delta_max": -0.1,  # Strictement négatif
        "default_tau": 0.0,
        "default_delta": -1.0,
    }


def layout_pedagogic() -> html.Div:
    """
    Retourne le contenu pédagogique pour la page Selle.
    """
    return html.Div(
        [
            html.P(
                "Un point selle est un équilibre instable dans certaines directions et stable dans d'autres. "
                "C'est un cas mixte où le système converge le long d'une direction et diverge le long d'une autre."
            ),
            html.H4("Exemple de la vie réelle :"),
            html.Ul(
                [
                    html.Li(
                        "Un ballon placé sur une selle: Si on pousse légèrement vers l'avant ou l'arrière, il roule dans ces directions. "
                        "Mais si on le pousse sur les côtés, il peut se stabiliser temporairement avant de retomber."
                    ),
                    html.Li(
                        "Un col de montagne: Les points cols sont des selles topologiques où vous êtes en bas dans une direction et en haut dans l'autre."
                    ),
                ]
            ),
            html.H4("Caractéristiques mathématiques:"),
            html.Ul(
                [
                    html.Li("Deux racines réelles de signes opposés"),
                    html.Li("Une racine positive (divergence)"),
                    html.Li("Une racine négative (convergence)"),
                    html.Li(
                        "Comportement: instable dans une direction, stable dans l'autre"
                    ),
                ]
            ),
        ]
    )


def register_callbacks(app) -> None:
    """
    Enregistre les callbacks pour la page Selle.
    """
    # Selle: Δ < 0
    register_stability_callbacks(
        app, PAGE_KEY, tau=0.0, delta=-1.0, create_phase_fig=create_figure
    )

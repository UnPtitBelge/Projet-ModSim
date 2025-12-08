from __future__ import annotations

import plotly.graph_objects as go
from dash import html  # type: ignore

from src.app.stabilite.base_callbacks import register_stability_callbacks
from src.app.stabilite.base_figures import create_phase_diagram
from src.app.stabilite.base_layout import build_stability_layout, stability_ids

# Clé de page pour "Centre"
PAGE_KEY = "ligne_pe_stable"

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
    Crée le diagramme de phase pour une ligne propre stable.
    Paramètres: a=-1, b=0, c=0, d=0
    """
    return create_phase_diagram(a=-1, b=0, c=0, d=0, title="Ligne propre stable")


def get_constraints() -> dict:
    """
    Retourne les contraintes pour les sliders pour une ligne de points d'équilibre stable.

    Ligne PE stable:
    - τ < 0 (trace négative)
    - Δ = 0 (déterminant nul)
    """
    return {
        "tau_min": -5.0,
        "tau_max": -0.1,
        "delta_min": -0.05,
        "delta_max": 0.05,
        "default_tau": -1.0,
        "default_delta": 0.0,
    }


def layout_pedagogic() -> html.Div:
    """
    Retourne le contenu pédagogique pour la page Ligne propre stable.
    """
    return html.Div(
        [
            html.P(
                "Une ligne propre stable est un point d'équilibre où les trajectoires convergent linéairement le long d'une ligne (direction propre)."
            ),
            html.H4("Exemple de la vie réelle :"),
            html.Ul(
                [
                    html.Li(
                        "Un bille dans une gouttière: Lorsqu'elle est perturbée légèrement, elle roule vers le bas de la gouttière et s'y stabilise."
                    ),
                    html.Li(
                        "Un amortisseur de voiture: L'amortissement de l'énergie conduit à la stabilité le long d'une direction privilégiée."
                    ),
                ]
            ),
            html.H4("Caractéristiques mathématiques:"),
            html.Ul(
                [
                    html.Li("Deux racines réelles"),
                    html.Li("Les deux racines sont négatives"),
                    html.Li("Convergence linéaire vers le point d'équilibre"),
                ]
            ),
        ]
    )


def register_callbacks(app) -> None:
    """
    Enregistre les callbacks pour la page Ligne PE stable.
    """
    # Ligne PE stable: τ < 0, Δ = 0
    register_stability_callbacks(
        app, PAGE_KEY, tau=-1.0, delta=0.0, create_phase_fig=create_figure
    )

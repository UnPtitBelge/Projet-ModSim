from __future__ import annotations

import plotly.graph_objects as go
from dash import html  # type: ignore

from src.app.stabilite.base_callbacks import register_stability_callbacks
from src.app.stabilite.base_figures import create_phase_diagram
from src.app.stabilite.base_layout import build_stability_layout, stability_ids

# Clé de page pour "Nœud stable dégénéré"
PAGE_KEY = "noeud_stable_degenere"

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
    Crée le diagramme de phase pour un nœud stable dégénéré.
    Paramètres: a=-1, b=1, c=0, d=-1
    """
    return create_phase_diagram(a=-1, b=1, c=0, d=-1, title="Nœud stable dégénéré")


def get_constraints() -> dict:
    """
    Retourne les contraintes pour les sliders pour un noeud stable dégénéré.

    Noeud stable dégénéré:
    - τ < 0 (trace négative)
    - Δ = τ²/4 (racine réelle double)
    """
    return {
        "tau_min": -5.0,
        "tau_max": -0.1,
        "delta_min": 0.01,
        "delta_max": 6.25,  # (-5)²/4 = 6.25
        "default_tau": -2.0,
        "default_delta": 1.0,  # 1 ≈ (-2)²/4 = 1
    }


def layout_pedagogic() -> html.Div:
    """
    Retourne le contenu pédagogique pour la page Nœud stable dégénéré.
    """
    return html.Div(
        [
            html.P(
                "Un nœud stable dégénéré est un point d'équilibre critique où les trajectoires convergent linéairement vers le point fixe avec une légère déformation de la trajectoire avant l'arrivée."
            ),
            html.H4("Exemple de la vie réelle :"),
            html.Ul(
                [
                    html.Li(
                        "Un système de ressorts parfaitement amortis: Le système revient à l'équilibre sans oscillations, le plus rapidement possible."
                    ),
                ]
            ),
            html.H4("Caractéristiques mathématiques:"),
            html.Ul(
                [
                    html.Li("Racines réelles multiples (dégénérées)"),
                    html.Li("Les deux racines sont négatives et égales"),
                    html.Li("Convergence linéaire dégénérée"),
                ]
            ),
        ]
    )


def register_callbacks(app) -> None:
    """
    Enregistre les callbacks pour la page Noeud stable dégénéré.
    """
    # Noeud stable dégénéré: τ < 0, Δ = τ²/4
    register_stability_callbacks(
        app, PAGE_KEY, tau=-2.0, delta=1.0, create_phase_fig=create_figure
    )

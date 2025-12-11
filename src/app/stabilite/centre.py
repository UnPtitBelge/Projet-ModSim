from __future__ import annotations

import plotly.graph_objects as go
from dash import html

from src.app.stabilite.base_callbacks import register_stability_callbacks
from src.app.stabilite.base_figures import create_phase_diagram
from src.app.stabilite.base_layout import build_stability_layout, stability_ids

# Clé de page pour "Centre"
PAGE_KEY = "centre"

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
    Crée le diagramme de phase pour un centre.
    Paramètres: a=0, b=1, c=-1, d=0
    """
    return create_phase_diagram(a=0, b=1, c=-1, d=0, title="Centre")


def get_constraints() -> dict:
    """
    Retourne les contraintes pour les sliders pour un centre.

    Centre:
    - τ = 0 (trace nulle)
    - Δ > 0 (déterminant positif)
    """
    return {
        "tau_min": -0.05,
        "tau_max": 0.05,  # Proche de zéro
        "delta_min": 0.1,
        "delta_max": 4.0,
        "default_tau": 0.0,
        "default_delta": 1.0,
    }


def layout_pedagogic() -> html.Div:
    """
    Retourne le contenu pédagogique pour la page Centre.
    """
    return html.Div(
        [
            html.P(
                "Un point d’équilibre est un centre lorsque les valeurs propres sont purement imaginaires. Les trajectoires sont alors des courbes fermées (cercles ou ellipses), traduisant un mouvement oscillatoire sans amortissement. L’équilibre est donc stable mais non asymptotiquement stable, car les trajectoires ne convergent pas vers le point d’équilibre."
            ),
            html.H4("Exemple de la vie réelle :"),
            html.Ul(
                [
                    html.Li(
                        "Un pendule dans le vide: Sans friction, un pendule oscille indéfiniment autour du point d'équilibre, ni divergent ni convergent."
                    ),
                    html.Li(
                        "Les orbites planétaires: Les planètes orbitent autour du soleil suivant des trajectoires fermées et stables, ce qui les maintient à une distance relativement constante du soleil."
                    ),
                ]
            ),
            html.H4("Caractéristiques mathématiques:"),
            html.Ul(
                [
                    html.Li("$\\tau$ = 0"),
                    html.Li("$\\Delta$ > 0"),
                    html.Li("Racines complexes pures"),
                    html.Li("Partie réelle nulle"),
                    html.Li("Comportement: oscillations perpétuelles"),
                ]
            ),
        ]
    )


def register_callbacks(app) -> None:
    """
    Enregistre les callbacks pour la page Centre.
    """
    # Centre: τ ≈ 0, Δ > 0
    register_stability_callbacks(
        app, PAGE_KEY, tau=0.0, delta=1.0, create_phase_fig=create_figure
    )

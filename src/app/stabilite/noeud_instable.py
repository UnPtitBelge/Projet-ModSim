from __future__ import annotations

import plotly.graph_objects as go
from dash import html  # type: ignore

from src.app.stabilite.base_callbacks import register_stability_callbacks
from src.app.stabilite.base_figures import create_phase_diagram
from src.app.stabilite.base_layout import build_stability_layout, stability_ids

# Clé de page pour "Centre"
PAGE_KEY = "noeud_instable"

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
    Crée le diagramme de phase pour un nœud instable.
    Paramètres: a=2, b=0, c=0, d=1
    """
    return create_phase_diagram(a=2, b=0, c=0, d=1, title="Nœud instable")


def get_constraints() -> dict:
    """
    Retourne les contraintes pour les sliders pour un noeud instable.

    Noeud instable:
    - τ > 0 (trace positive)
    - 0 < Δ < τ²/4 (racines réelles distinctes)
    """
    return {
        "tau_min": 0.1,  # Strictement positif
        "tau_max": 5.0,
        "delta_min": 0.1,
        "delta_max": 2.0,
        "default_tau": 3.0,
        "default_delta": 1.0,
    }


def layout_pedagogic() -> html.Div:
    """
    Retourne le contenu pédagogique pour la page Nœud instable.
    """
    return html.Div(
        [
            html.P(
                "Un nœud instable est un point d'équilibre où les trajectoires s'éloignent du point dans toutes les directions sans oscillations."
            ),
            html.H4("Exemple de la vie réelle :"),
            html.Ul(
                [
                    html.Li(
                        "Un ballon de football surmonté d'une épine: Lorsqu'on place le ballon en équilibre sur l'épine et qu'on le perturbe, il roule dans une direction quelconque et s'éloigne indéfiniment."
                    ),
                    html.Li(
                        "Une réaction nucléaire incontrôlée: La réaction s'accélère exponentiellement et s'éloigne de l'équilibre initial."
                    ),
                ]
            ),
            html.H4("Caractéristiques mathématiques:"),
            html.Ul(
                [
                    html.Li("$\\tau$ < 0"),
                    html.Li("0 < $\\Delta$ < $\\tau^2/4$"),
                    html.Li("Deux racines réelles positives"),
                    html.Li("Instable non oscillatoire"),
                ]
            ),
        ]
    )


def register_callbacks(app) -> None:
    """
    Enregistre les callbacks pour la page Noeud instable.
    """
    # Noeud instable: τ > 0, 0 < Δ < τ²/4
    register_stability_callbacks(
        app, PAGE_KEY, tau=3.0, delta=1.0, create_phase_fig=create_figure
    )

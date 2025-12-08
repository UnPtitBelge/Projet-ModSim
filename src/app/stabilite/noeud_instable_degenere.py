from __future__ import annotations

import plotly.graph_objects as go
from dash import html  # type: ignore

from src.app.stabilite.base_callbacks import register_stability_callbacks
from src.app.stabilite.base_figures import create_phase_diagram
from src.app.stabilite.base_layout import build_stability_layout, stability_ids

# Clé de page pour "Nœud instable dégénéré"
PAGE_KEY = "noeud_instable_degenere"

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
    Crée le diagramme de phase pour un nœud instable dégénéré.
    Paramètres: a=1, b=-1, c=0, d=1
    """
    return create_phase_diagram(a=1, b=-1, c=0, d=1, title="Nœud instable dégénéré")


def get_constraints() -> dict:
    """
    Retourne les contraintes pour les sliders pour un noeud instable dégénéré.

    Noeud instable dégénéré:
    - τ > 0 (trace positive)
    - Δ = τ²/4 (racine réelle double)
    """
    return {
        "tau_min": 0.1,
        "tau_max": 5.0,
        "delta_min": 0.01,
        "delta_max": 6.25,
        "default_tau": 2.0,
        "default_delta": 1.0,
    }


def layout_pedagogic() -> html.Div:
    """
    Retourne le contenu pédagogique pour la page Nœud instable dégénéré.
    """
    return html.Div(
        [
            html.P(
                "Un nœud instable dégénéré est un point d'équilibre critique où les trajectoires divergent linéairement dans une direction dégénérée."
            ),
            html.H4("Exemple de la vie réelle :"),
            html.Ul(
                [
                    html.Li(
                        "Un système laser critique: À un point critique du laser, des perturbations mineures peuvent causer une divergence dégénérée de l'émission."
                    ),
                    html.Li(
                        "Une pile instable: Une pile de blocs où une perturbation au sommet cause une chute dans une direction préférentielle."
                    ),
                ]
            ),
            html.H4("Caractéristiques mathématiques:"),
            html.Ul(
                [
                    html.Li("Cas critique avec racines multiples"),
                    html.Li("Divergence linéaire dégénérée"),
                    html.Li("Comportement instable non oscillatoire"),
                ]
            ),
        ]
    )


def register_callbacks(app) -> None:
    """
    Enregistre les callbacks pour la page Noeud instable dégénéré.
    """
    # Noeud instable dégénéré: τ > 0, Δ = τ²/4
    register_stability_callbacks(
        app, PAGE_KEY, tau=2.0, delta=1.0, create_phase_fig=create_figure
    )

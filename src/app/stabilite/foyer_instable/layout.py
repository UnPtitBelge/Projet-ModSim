from __future__ import annotations
from typing import Optional

from dash import html, Input, Output  # type: ignore

from src.app.stabilite.base_callbacks import register_stability_callbacks
from src.app.stabilite.base_layout import build_stability_layout, stability_ids

# Clé de page pour "Centre"
PAGE_KEY = "foyer_instable"

__all__ = [
    "PAGE_KEY",
    "get_ids",
    "build_layout",
    "register_callbacks",
]


def get_ids() -> dict[str, str]:
    """
    Retourne les IDs normalisés des placeholders pour la page Centre.
    - graph: ID du graphique interactif
    - phase: ID du diagramme de phase
    - explication: ID du bloc d'explication pédagogique
    """
    return stability_ids(PAGE_KEY)


def build_layout() -> html.Div:
    """
    Construit le layout minimal pour la page Centre:
    - Graphique interactif (dcc.Graph)
    - Diagramme de phase (dcc.Graph)
    - Explication pédagogique (html.Div)
    """
    return build_stability_layout(PAGE_KEY)


def register_callbacks(app) -> None:
    """
    Enregistre les callbacks de base pour remplir les placeholders de la page Centre.
    Strict nécessaire: figures et explication "à compléter".
    """
    ids = stability_ids(PAGE_KEY)

    @app.callback(
        Output(ids["explication"], "children"),
        Input(ids["explication"], "id"),
        prevent_initial_call=False,
    )
    def _update_explication(_explication_id: str):
        return [
            html.P(
                "Un foyer instable est un point d'équilibre où les trajectoires s'éloignent en suivant des spirales autour de celui-ci lorsqu'une petite perturbation se produit."
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

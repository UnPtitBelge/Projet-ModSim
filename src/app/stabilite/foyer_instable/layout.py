from __future__ import annotations

from dash import html  # type: ignore

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
    register_stability_callbacks(app, PAGE_KEY)

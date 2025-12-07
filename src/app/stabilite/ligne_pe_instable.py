from __future__ import annotations

from dash import html  # type: ignore

from src.app.stabilite.base_callbacks import register_stability_callbacks
from src.app.stabilite.base_layout import build_stability_layout, stability_ids

# Clé de page pour "Centre"
PAGE_KEY = "ligne_pe_instable"

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


def layout_pedagogic() -> html.Div:
    """
    Retourne le contenu pédagogique pour la page Ligne propre instable.
    """
    return html.Div([
        html.P(
            "Une ligne propre instable est un point d'équilibre où les trajectoires divergent linéairement le long d'une ligne (direction propre)."
        ),
        html.H4("Exemple de la vie réelle :"),
        html.Ul(
            [
                html.Li(
                    "Un bâton placé verticalement en équilibre instable: Une petite perturbation le fait tomber dans une direction préférentielle."
                ),
                html.Li(
                    "La bifurcation pitchfork: Certains systèmes bifurquent vers plusieurs états instables à partir d'un point d'équilibre initial."
                ),
            ]
        ),
        html.H4("Caractéristiques mathématiques:"),
        html.Ul(
            [
                html.Li("Deux racines réelles"),
                html.Li("Au moins une racine positive"),
                html.Li("Convergence sur une ligne, divergence dans autres directions"),
            ]
        ),
    ])

def register_callbacks(app) -> None:
    """
    Enregistre les callbacks de base pour remplir les placeholders de la page Centre.
    Strict nécessaire: figures et explication "à compléter".
    """
    register_stability_callbacks(app, PAGE_KEY)

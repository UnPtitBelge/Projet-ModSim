from __future__ import annotations

from dash import html  # type: ignore

from src.app.stabilite.base_callbacks import register_stability_callbacks
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


def layout_pedagogic() -> html.Div:
    """
    Retourne le contenu pédagogique pour la page Centre.
    """
    return html.Div([
        html.P(
            "Un centre est un point d'équilibre neutre où les trajectoires s'arrangent autour de celui-ci sans converger ni s'éloigner. "
            "Le système oscille indéfiniment sans amortissement ni amplification."
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
    ])

def register_callbacks(app) -> None:
    """
    Enregistre les callbacks de base pour remplir les placeholders de la page Centre.
    Strict nécessaire: figures et explication "à compléter".
    """
    register_stability_callbacks(app, PAGE_KEY)

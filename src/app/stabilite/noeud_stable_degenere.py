from __future__ import annotations

from dash import html  # type: ignore

from src.app.stabilite.base_callbacks import register_stability_callbacks
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


def layout_pedagogic() -> html.Div:
    """
    Retourne le contenu pédagogique pour la page Nœud stable dégénéré.
    """
    return html.Div([
        html.P(
            "Un nœud stable dégénéré est un point d'équilibre critique où les trajectoires convergent linéairement vers le point fixe de façon dégénérée."
        ),
        html.H4("Exemple de la vie réelle :"),
        html.Ul(
            [
                html.Li(
                    "Un système de ressorts parfaitement amortis: Le système revient à l'équilibre de façon critique sans dépasser."
                ),
                html.Li(
                    "L'amortissement critique d'une suspension automobile: La voiture revient à sa position d'équilibre sans oscillations, le plus rapidement possible."
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
    ])

def register_callbacks(app) -> None:
    """
    Enregistre les callbacks de base pour remplir les placeholders de la page Centre.
    Strict nécessaire: figures et explication "à compléter".
    """
    register_stability_callbacks(app, PAGE_KEY)

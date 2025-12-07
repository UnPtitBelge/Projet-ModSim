from __future__ import annotations
from typing import Optional

from dash import html, Input, Output  # type: ignore

from src.app.stabilite.base_callbacks import register_stability_callbacks
from src.app.stabilite.base_layout import build_stability_layout, stability_ids

# Clé de page pour "Centre"
PAGE_KEY = "noeud_stable"

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
    Retourne le contenu pédagogique pour la page Nœud stable.
    """
    return html.Div([
        html.P("Etat d'équilibre asymptotiquement stable où les trajectoires convergent vers le point fixe sans oscillations."),
        html.H4("Exemple de la vie réelle :"),
        html.Ul(
            [
                html.Li("Une bille placée au bord d'une cuvette, qui va rouler vers le fond de celle-ci et s'y stabiliser sans oscillations lorsqu'on la perturbe légèrement, le fond de la cuvette représentant un noeud stable."),
                html.Li("Le cruise control d'une voiture : Lorsqu'on active le cruise control, le système ajuste automatiquement la vitesse de la voiture pour maintenir la vitesse cible constante. Si la voiture ralentit légèrement, le système augmente la puissance pour revenir à la vitesse définie, et vice versa, assurant ainsi une stabilité sans oscillations autour de la vitesse choisie."),
            ]
        ),
        html.H4("Caractéristiques mathématiques:"),
        html.Ul(
            [
                html.Li("$\\tau$ > 0"),
                html.Li("0 < $\\Delta$ < $\\tau^2/4$"),
                html.Li("Deux racines réelles négatives"),
                html.Li("Stable non oscillatoire"),
            ]
        ),
    ])

def register_callbacks(app) -> None:
    """
    Enregistre les callbacks de base pour remplir les placeholders de la page Centre.
    Strict nécessaire: figures et explication "à compléter".
    """
    register_stability_callbacks(app, PAGE_KEY)


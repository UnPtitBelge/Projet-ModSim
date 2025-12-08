from __future__ import annotations

import plotly.graph_objects as go
from dash import html  # type: ignore

from src.app.stabilite.base_callbacks import register_stability_callbacks
from src.app.stabilite.base_layout import build_stability_layout, stability_ids
from src.app.stabilite.base_figures import create_phase_diagram

# Clé de page pour "Mouvement uniforme"
PAGE_KEY = "mouvement_uniforme"

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
    Crée le diagramme de phase pour un mouvement uniforme.
    Paramètres: a=0, b=1, c=0, d=0
    """
    return create_phase_diagram(a=0, b=1, c=0, d=0, title="Mouvement uniforme")


def layout_pedagogic() -> html.Div:
    """
    Retourne le contenu pédagogique pour la page Mouvement uniforme.
    """
    return html.Div([
        html.P(
            "Un mouvement uniforme est un cas limite où le point d'équilibre n'existe pas ou est dégénéré. "
            "Le système se déplace à une vitesse constante sans accélération."
        ),
        html.H4("Exemple de la vie réelle :"),
        html.Ul(
            [
                html.Li(
                    "Une voiture roulant à vitesse constante: En l'absence de forces externes (frottement, air), le système maintient une vitesse constante."
                ),
                html.Li(
                    "Un objet flottant dans l'espace: Un objet sans forces extérieures continue à se déplacer à vitesse uniforme."
                ),
            ]
        ),
        html.H4("Caractéristiques mathématiques:"),
        html.Ul(
            [
                html.Li("Cas critique: une ou deux racines nulles"),
                html.Li("Pas de convergence vers un équilibre"),
                html.Li("Trajectoires parallèles et linéaires"),
            ]
        ),
    ])

def register_callbacks(app) -> None:
    """
    Enregistre les callbacks de base pour remplir les placeholders de la page Mouvement uniforme.
    Strict nécessaire: figures et explication "à compléter".
    """
    register_stability_callbacks(app, PAGE_KEY, create_figure)

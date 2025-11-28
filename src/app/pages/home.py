"""
Page d'accueil (home) de l'application multipage Projet-ModSim.

Cette page fournit :
- Une introduction générale au diagramme de Poincaré et à l'analyse de stabilité
- Des liens rapides vers les pages principales (Diagramme, Sommaire stabilité, À propos)
- Un aperçu pédagogique des paramètres Tau (τ) et Delta (Δ)
- Un chemin d'exploration conseillé

Usage:
    Dash découvre automatiquement cette page grâce à dash.register_page lorsque
    l'application est lancée avec use_pages=True dans app.py.

Note:
    La route racine "/" est déjà utilisée par la page du diagramme de Poincaré.
    Cette page d'accueil est donc exposée sous le chemin "/home".
"""

from __future__ import annotations

import dash
from dash import html

# Enregistrement de la page (multipage)
dash.register_page(
    __name__,
    path="/",
    name="Accueil",
    title="Accueil – Projet ModSim",
    description="Page d'accueil, introduction et navigation globale.",
    order=-1,  # affiche l'accueil avant les autres pages dans la barre de navigation
)

# Contenu principal
layout = html.Div(
    [
        html.H1("Accueil – Analyse de stabilité de systèmes du second ordre"),
        html.P(
            (
                "Bienvenue dans l'application d'exploration du diagramme de Poincaré. "
                "Cet outil interactif permet de visualiser et comprendre les zones de stabilité "
                "associées à l'équation caractéristique λ² + τλ + Δ = 0 pour des systèmes linéaires continus "
                "d'ordre deux. Les paramètres τ (Tau) et Δ (Delta) structurent la dynamique des solutions."
            )
        ),
        html.H2("Objectifs pédagogiques"),
        html.Ul(
            [
                html.Li(
                    "Visualiser la séparation des régimes (oscillatoire, amorti, divergent)."
                ),
                html.Li(
                    "Relier la position (τ, Δ) aux racines du polynôme caractéristique."
                ),
                html.Li("Identifier rapidement les zones de stabilité locale."),
                html.Li(
                    "Explorer les effets des variations de τ et Δ via une représentation géométrique."
                ),
            ]
        ),
        html.H2("Navigation rapide"),
        html.Ul(
            [
                html.Li(
                    html.A("Diagramme de Poincaré (page principale)", href="/poincare")
                ),
                html.Li(html.A("Sommaire des zones de stabilité", href="/stabilite")),
                html.Li(html.A("À propos du projet", href="/about")),
            ]
        ),
        html.H2("Tau (τ) et Delta (Δ) – rappel"),
        html.P(
            (
                "Dans l'équation λ² + τλ + Δ = 0, les racines λ déterminent la nature de la réponse temporelle. "
                "La parabole Δ = τ²/4 sépare les régimes à racines réelles (sous) des régimes à racines complexes "
                "(au-dessus). Le signe de τ contrôle la partie réelle des racines complexes (amortissement vs divergence). "
                "Le signe de Δ influence la nature 'selle' (Δ < 0) ou ‘non oscillatoire’ (Δ > 0, sous la parabole)."
            )
        ),
        html.H2("Chemin recommandé"),
        html.Ol(
            [
                html.Li("Observer la forme générale du diagramme (page principale)."),
                html.Li(
                    "Cliquer sur différentes zones pour voir les descriptions spécifiques."
                ),
                html.Li(
                    "Visiter le sommaire stabilité pour synthétiser les classifications."
                ),
                html.Li(
                    "Lire la page À propos pour comprendre la structure du projet."
                ),
            ]
        ),
        html.H2("Ressources futures (placeholder)"),
        html.Ul(
            [
                html.Li(
                    "Ajout prévu : visualisation dynamique des trajectoires temporelles."
                ),
                html.Li("Comparaison multi-paramètres (surfaces 3D éventuelles)."),
                html.Li("Export des zones ou figures en image."),
            ]
        ),
        html.Hr(),
        html.Div(
            [
                html.A(
                    "→ Accéder au diagramme",
                    href="/poincare",
                    style={"marginRight": "18px"},
                ),
                html.A(
                    "→ Sommaire stabilité",
                    href="/stabilite",
                    style={"marginRight": "18px"},
                ),
                html.A("→ À propos", href="/about"),
            ],
            style={"marginTop": "8px"},
        ),
        html.Div(
            "Projet-ModSim – Exploration de stabilité (version initiale)",
            style={
                "marginTop": "30px",
                "fontSize": "0.8rem",
                "color": "#666",
            },
        ),
    ],
    style={
        "maxWidth": "960px",
        "padding": "32px 36px",
        "fontFamily": "Arial, sans-serif",
        "lineHeight": "1.5",
        "fontSize": "0.95rem",
    },
)


def get_home_layout():
    """
    Fournit le layout de la page d'accueil (utilitaire externe éventuel).
    """
    return layout

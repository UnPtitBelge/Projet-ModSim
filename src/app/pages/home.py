from __future__ import annotations

import dash
from dash import html

from src.app.style.components.layout import app_container, page_text_container
from src.app.style.text import TEXT

dash.register_page(
    __name__,
    path="/",
    name="Accueil",
    title="Accueil – Projet ModSim",
    description="Page d'accueil, introduction et navigation globale.",
    order=-1,  # affiche l'accueil avant les autres pages dans la barre de navigation
)


layout = html.Div(
    [
        html.H1(
            "Accueil – Analyse de stabilité de systèmes du second ordre",
            style=TEXT["h1"],
        ),
        html.Div(
            "$$\\lambda^2 + \\tau\\lambda + \\Delta = 0$$", style={"marginTop": "8px"}
        ),
        html.P(
            (
                "Bienvenue dans l'application d'exploration du diagramme de Poincaré. "
                "Cet outil interactif permet de visualiser et comprendre les zones de stabilité "
                "pour des systèmes linéaires continus d'ordre deux."
            )
        ),
        html.H2("Objectifs pédagogiques"),
        html.Ul(
            [
                html.Li(
                    "Visualiser la séparation des régimes (oscillatoire, amorti, divergent)."
                ),
                html.Li(
                    "Relier la position $(\\tau, \\Delta)$ aux racines du polynôme caractéristique."
                ),
                html.Div(
                    "$$\\text{Position sur le plan } (\\tau,\\Delta) \\Rightarrow \\text{ nature des racines } \\lambda$$"
                ),
                html.Li("Identifier rapidement les zones de stabilité locale."),
                html.Li(
                    "Explorer les effets des variations de $\\tau$ et $\\Delta$ via une représentation géométrique."
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
        html.H2("Rappel des paramètres"),
        html.Div("$$\\lambda^2 + \\tau\\lambda + \\Delta = 0$$"),
        html.Div("$$\\Delta = \\tau^2/4$$"),
        html.P(
            (
                "Les racines $\\lambda$ déterminent la nature de la réponse temporelle. "
                "La relation ci-dessus sépare les régimes à racines réelles (sous) et complexes (au-dessus). "
                "Le signe de $\\tau$ contrôle la partie réelle (amortissement vs divergence) et "
                "le signe de $\\Delta$ influence la nature 'selle' ($\\Delta < 0$) ou ‘non oscillatoire’ ($\\Delta > 0$)."
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
        **app_container(),
        **page_text_container(960),
        "padding": "32px 36px",
    },
)


def get_home_layout():
    return layout

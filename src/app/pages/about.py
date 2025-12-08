import dash
from dash import html

from src.app.style.components.layout import (app_container, content_wrapper,
                                             section_card)
from src.app.style.palette import PALETTE
from src.app.style.text import TEXT

dash.register_page(
    __name__,
    path="/about",
    name="À propos",
    title="À propos – Stabilité des systèmes linéaires",
    order=1,
    description="Contexte et objectifs du dashboard pédagogique sur la stabilité.",
)

layout = html.Div(
    [
        html.Div(
            [
                html.H1("À propos de ce dashboard", style=TEXT["h1"]),
                html.P(
                    (
                        "Ce dashboard pédagogique est conçu pour offrir un support théorique "
                        "et interactif autour de la notion de stabilité des systèmes dynamiques. "
                        "Il se concentre sur les systèmes linéaires continus d'ordre 2 et "
                        "leurs différents types de points d'équilibre."
                    ),
                    style=TEXT["p"],
                ),
            ],
            style=section_card(),
        ),
        html.Div(
            [
                html.H2("Objectif pédagogique", style=TEXT["h2"]),
                html.P(
                    (
                        "L'objectif principal est de permettre aux étudiants et enseignants "
                        "de visualiser et comprendre les liens entre :"
                    ),
                    style=TEXT["p"],
                ),
                html.Ul(
                    [
                        html.Li(
                            "Les paramètres du système : trace $\\tau$ et déterminant $\\Delta$",
                            style=TEXT["p"],
                        ),
                        html.Li(
                            "La nature des valeurs propres du système",
                            style=TEXT["p"],
                        ),
                        html.Li(
                            "Le comportement dynamique : convergence, divergence, oscillations",
                            style=TEXT["p"],
                        ),
                        html.Li(
                            "La stabilité locale du point d'équilibre",
                            style=TEXT["p"],
                        ),
                    ],
                ),
            ],
            style=section_card(),
        ),
        html.Div(
            [
                html.H2("Contenu du dashboard", style=TEXT["h2"]),
                html.H3("Diagramme de Poincaré", style=TEXT["h3"]),
                html.P(
                    (
                        "Le diagramme de Poincaré est une représentation dans le plan $(\\tau, \\Delta)$ "
                        "qui divise l'espace en zones correspondant aux 11 types de points d'équilibre. "
                        "Chaque zone est colorée et cliquable pour accéder aux détails."
                    ),
                    style=TEXT["p"],
                ),
                html.H3("Pages de stabilité", style=TEXT["h3"]),
                html.P(
                    (
                        "Chaque type de point d'équilibre dispose d'une page dédiée comprenant :"
                    ),
                    style=TEXT["p"],
                ),
                html.Ul(
                    [
                        html.Li(
                            "Un graphique interactif permettant de modifier les paramètres",
                            style=TEXT["p"],
                        ),
                        html.Li(
                            "Un portrait de phase montrant les trajectoires du système",
                            style=TEXT["p"],
                        ),
                        html.Li(
                            "Des explications théoriques et exemples concrets",
                            style=TEXT["p"],
                        ),
                        html.Li(
                            "Les caractéristiques mathématiques du point d'équilibre",
                            style=TEXT["p"],
                        ),
                    ],
                ),
            ],
            style=section_card(),
        ),
        html.Div(
            [
                html.H2("Structure technique", style=TEXT["h2"]),
                html.P(
                    "Le dashboard est structuré en modules pour faciliter la maintenance et l'extension :",
                    style=TEXT["p"],
                ),
                html.Ul(
                    [
                        html.Li(
                            [
                                html.Code("src/app/app.py", style=TEXT["code_block"]),
                                " : point d'entrée de l'application multi-page",
                            ],
                            style=TEXT["p"],
                        ),
                        html.Li(
                            [
                                html.Code(
                                    "src/app/poincare/", style=TEXT["code_block"]
                                ),
                                " : modules du diagramme de Poincaré",
                            ],
                            style=TEXT["p"],
                        ),
                        html.Li(
                            [
                                html.Code(
                                    "src/app/stabilite/", style=TEXT["code_block"]
                                ),
                                " : logique des pages de stabilité",
                            ],
                            style=TEXT["p"],
                        ),
                        html.Li(
                            [
                                html.Code("src/app/style/", style=TEXT["code_block"]),
                                " : système de design centralisé",
                            ],
                            style=TEXT["p"],
                        ),
                    ],
                ),
            ],
            style=section_card(),
        ),
        html.Div(
            [
                html.H2("Technologies utilisées", style=TEXT["h2"]),
                html.Ul(
                    [
                        html.Li(
                            "Dash / Plotly : framework web interactif Python",
                            style=TEXT["p"],
                        ),
                        html.Li(
                            "NumPy / SciPy : calculs numériques et intégration d'EDO",
                            style=TEXT["p"],
                        ),
                        html.Li(
                            "MathJax : rendu des équations mathématiques",
                            style=TEXT["p"],
                        ),
                    ],
                ),
            ],
            style=section_card(),
        ),
        html.Div(
            [
                html.A(
                    "← Retour à l'accueil",
                    href="/",
                    style={
                        "display": "inline-block",
                        "padding": "10px 20px",
                        "backgroundColor": PALETTE.surface,
                        "color": PALETTE.primary,
                        "textDecoration": "none",
                        "borderRadius": "8px",
                        "border": f"2px solid {PALETTE.primary}",
                        "fontWeight": "600",
                        "marginRight": "12px",
                    },
                ),
                html.A(
                    "→ Accéder au diagramme",
                    href="/poincare",
                    style={
                        "display": "inline-block",
                        "padding": "10px 20px",
                        "backgroundColor": PALETTE.primary,
                        "color": PALETTE.surface,
                        "textDecoration": "none",
                        "borderRadius": "8px",
                        "fontWeight": "600",
                    },
                ),
            ],
            style=section_card(),
        ),
    ],
    style={
        **app_container(),
        **content_wrapper(),
    },
)

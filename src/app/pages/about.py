import dash
from dash import html

from src.app.style.components.layout import (app_container, content_wrapper,
                                             section_card, nav_button, spacing_section)
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
                html.H3("Diagramme de Poincaré interactif", style=TEXT["h3"]),
                html.P(
                    (
                        "Le diagramme de Poincaré est une représentation dans le plan $(\\tau, \\Delta)$ "
                        "qui divise l'espace en zones correspondant aux 11 types de points d'équilibre. "
                        "Chaque zone est colorée et interactive : survolez pour identifier, cliquez pour explorer."
                    ),
                    style=TEXT["p"],
                ),
                html.H3("Affichage inline des détails", style=TEXT["h3"]),
                html.P(
                    (
                        "En cliquant sur une zone du diagramme de Poincaré, les détails complets s'affichent "
                        "directement sur la même page, incluant :"
                    ),
                    style=TEXT["p"],
                ),
                html.Ul(
                    [
                        html.Li(
                            "Les valeurs des paramètres $\\tau$ (trace) et $\\Delta$ (déterminant)",
                            style=TEXT["p"],
                        ),
                        html.Li(
                            "Les équations différentielles du système linéaire",
                            style=TEXT["p"],
                        ),
                        html.Li(
                            "Le calcul et la nature des valeurs propres",
                            style=TEXT["p"],
                        ),
                        html.Li(
                            "Le portrait de phase avec trajectoires, vecteurs propres et isoclines",
                            style=TEXT["p"],
                        ),
                        html.Li(
                            "L'évolution temporelle des variables d'état",
                            style=TEXT["p"],
                        ),
                        html.Li(
                            "Des explications théoriques et exemples concrets de la vie réelle",
                            style=TEXT["p"],
                        ),
                    ],
                ),
                html.H3("Exploration paramétrique", style=TEXT["h3"]),
                html.P(
                    (
                        "La page d'analyse interactive permet d'ajuster librement les paramètres $\\tau$ et $\\Delta$ "
                        "à l'aide de curseurs pour observer en temps réel l'impact sur le comportement du système."
                    ),
                    style=TEXT["p"],
                ),
            ],
            style=section_card(),
        ),
        html.Div(
            [
                html.H2("Architecture technique", style=TEXT["h2"]),
                html.P(
                    "Le dashboard est conçu selon une architecture modulaire et maintenable :",
                    style=TEXT["p"],
                ),
                html.Ul(
                    [
                        html.Li(
                            [
                                html.Code("src/app/app.py", style=TEXT["code_block"]),
                                " : application Dash multi-page avec sidebar de navigation",
                            ],
                            style=TEXT["p"],
                        ),
                        html.Li(
                            [
                                html.Code(
                                    "src/app/poincare/", style=TEXT["code_block"]
                                ),
                                " : diagramme interactif avec callbacks pour affichage inline",
                            ],
                            style=TEXT["p"],
                        ),
                        html.Li(
                            [
                                html.Code(
                                    "src/app/stabilite/", style=TEXT["code_block"]
                                ),
                                " : génération statique des layouts de stabilité (valeurs propres, EDO, portraits de phase)",
                            ],
                            style=TEXT["p"],
                        ),
                        html.Li(
                            [
                                html.Code("src/app/style/", style=TEXT["code_block"]),
                                " : design system centralisé (palette, typographie, composants)",
                            ],
                            style=TEXT["p"],
                        ),
                    ],
                ),
                html.P(
                    (
                        "L'architecture privilégie la réutilisabilité : les layouts de stabilité sont générés "
                        "par une fonction unique qui calcule toutes les données (eigenvalues, figures) sans callbacks, "
                        "permettant leur utilisation inline et standalone."
                    ),
                    style=TEXT["p"],
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
                    "→ Accéder au diagramme de Poincaré",
                    href="/poincare",
                    style=nav_button("primary"),
                ),
                html.A(
                    "→ Voir le sommaire de stabilité",
                    href="/stabilite",
                    style=nav_button("secondary"),
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

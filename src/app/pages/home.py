from __future__ import annotations

import dash
from dash import html

from src.app.style.components.layout import (app_container, content_wrapper,
                                             section_card, nav_button, spacing_section)
from src.app.style.palette import PALETTE
from src.app.style.text import TEXT

dash.register_page(
    __name__,
    path="/",
    name="Accueil",
    title="Accueil – Stabilité des systèmes linéaires",
    description="Support pédagogique pour l'analyse de stabilité des systèmes linéaires continus d'ordre 2.",
    order=-1,
)

layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "Analyse de stabilité des systèmes linéaires d'ordre 2",
                    style=TEXT["h1"],
                ),
                html.P(
                    (
                        "Bienvenue dans ce dashboard pédagogique dédié à l'étude de la stabilité "
                        "des systèmes linéaires continus d'ordre deux. Cet outil interactif vous permet "
                        "de comprendre et visualiser les différents types de points d'équilibre "
                        "et leur comportement dynamique."
                    ),
                    style=TEXT["p"],
                ),
            ],
            style=section_card(),
        ),
        html.Div(
            [
                html.H2("Contexte théorique", style=TEXT["h2"]),
                html.P(
                    (
                        "Pour un système linéaire d'ordre 2, l'équation caractéristique s'écrit :"
                    ),
                    style=TEXT["p"],
                ),
                html.Div(
                    "$$\\lambda^2 - \\tau\\lambda + \\Delta = 0$$",
                    style={"textAlign": "center", "margin": "16px 0"},
                ),
                html.P(
                    (
                        "où $\\tau$ est la trace de la matrice du système et $\\Delta$ son déterminant. "
                        "Les racines $\\lambda$ de cette équation déterminent complètement "
                        "la nature du point d'équilibre et sa stabilité."
                    ),
                    style=TEXT["p"],
                ),
            ],
            style=section_card(),
        ),
        html.Div(
            [
                html.H2("Objectifs pédagogiques", style=TEXT["h2"]),
                html.Ul(
                    [
                        html.Li(
                            "Comprendre le lien entre les paramètres $(\\tau, \\Delta)$ et la stabilité du système",
                            style=TEXT["p"],
                        ),
                        html.Li(
                            "Identifier les 11 types de points d'équilibre dans le plan de Poincaré",
                            style=TEXT["p"],
                        ),
                        html.Li(
                            "Visualiser les portraits de phase associés à chaque type d'équilibre",
                            style=TEXT["p"],
                        ),
                        html.Li(
                            "Distinguer les comportements : oscillatoire, amorti, divergent, stable, instable",
                            style=TEXT["p"],
                        ),
                    ],
                ),
            ],
            style=section_card(),
        ),
        html.Div(
            [
                html.H2("Types de points d'équilibre étudiés", style=TEXT["h2"]),
                html.P(
                    "Ce dashboard couvre l'ensemble des cas possibles :",
                    style=TEXT["p"],
                ),
                html.Ul(
                    [
                        html.Li("Foyer stable et instable", style=TEXT["p"]),
                        html.Li("Nœud stable et instable", style=TEXT["p"]),
                        html.Li("Nœud dégénéré stable et instable", style=TEXT["p"]),
                        html.Li("Centre", style=TEXT["p"]),
                        html.Li("Point selle", style=TEXT["p"]),
                        html.Li(
                            "Ligne de points d'équilibre stable et instable",
                            style=TEXT["p"],
                        ),
                        html.Li("Mouvement uniforme", style=TEXT["p"]),
                    ],
                ),
            ],
            style=section_card(),
        ),
        html.Div(
            [
                html.H2("Navigation", style=TEXT["h2"]),
                html.P(
                    "Explorez le dashboard dans l'ordre suivant :",
                    style=TEXT["p"],
                ),
                html.Ol(
                    [
                        html.Li(
                            [
                                html.A(
                                    "Diagramme de Poincaré",
                                    href="/poincare",
                                    style={"color": PALETTE.primary},
                                ),
                                " : vue d'ensemble interactive des zones de stabilité",
                            ],
                            style=TEXT["p"],
                        ),
                        html.Li(
                            "Cliquez sur une zone pour accéder aux détails du point d'équilibre correspondant",
                            style=TEXT["p"],
                        ),
                        html.Li(
                            [
                                html.A(
                                    "Sommaire des zones",
                                    href="/stabilite",
                                    style={"color": PALETTE.primary},
                                ),
                                " : synthèse complète des 11 types",
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
                html.Div(
                    [
                        html.A(
                            "→ Accéder au diagramme de Poincaré",
                            href="/poincare",
                            style=nav_button("primary"),
                        ),
                        html.A(
                            "→ Voir le sommaire",
                            href="/stabilite",
                            style=nav_button("secondary"),
                        ),
                    ],
                    style=spacing_section("top"),
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

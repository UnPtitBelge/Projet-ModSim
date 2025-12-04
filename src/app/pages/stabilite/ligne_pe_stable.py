"""
Page de stabilité: ligne de points d’équilibre stable

Cette page est enregistrée automatiquement par Dash (multipage natif).
URL sans accents et avec tirets pour cohérence avec la navigation par clic.
Contenu placeholder pour développement futur.
"""

from __future__ import annotations

import dash
from dash import html

from src.app.logging_setup import get_logger

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/ligne_pe_stable.")

dash.register_page(
    __name__,
    path="/stabilite/ligne_pe_stable",
    name="Stabilité (ligne de PE stable)",
    title="Stabilité – Ligne de points d’équilibre stable",
    order=19,
    description="Informations sur la ligne de points d’équilibre stable (placeholder).",
)

log.debug("Construction du layout de la page ligne de points d’equilibre stable...")

layout = html.Div(
    [
        html.Small(
            [
                html.A("Stabilité", href="/stabilite"),
                "  /  ",
                html.Span("Ligne de points d’équilibre stable"),
            ],
            style={"color": "#666"},
        ),
        html.H2("Ligne de points d’equilibre stable"),


        html.Div(
            [
                html.H3("À venir"),
                html.P(
                    [
                        "Contenu détaillé en préparation. Consultez la ",
                        html.A("roadmap du projet (PDF)", href="/docs/projet_2025_2026.pdf"),
                        ".",
                    ]
                ),
            ],
            style={"marginTop": "12px"}
        ),
        html.Hr(),
        html.Div(
            [
                html.A("← Retour au sommaire Stabilité", href="/stabilite"),
                html.Span("  |  "),
                html.A("Retour au diagramme de Poincaré", href="/poincare"),
            ],
            style={"marginTop": "10px"},
        ),
    ],
    style={
        "maxWidth": "900px",
        "padding": "24px",
        "fontFamily": "Arial, sans-serif",
        "lineHeight": "1.45",
        "fontSize": "0.95rem",
    },
)

log.info("Layout de la page ligne de points d’equilibre stable construit.")

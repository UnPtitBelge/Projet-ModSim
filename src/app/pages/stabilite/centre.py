"""
Page de stabilité: centre (tau = 0, delta > 0, racines purement imaginaires)

Cette page est enregistrée automatiquement par Dash (multipage natif).
URL sans accents et avec tirets pour cohérence avec la navigation par clic.
Contenu placeholder pour développement futur.
"""

from __future__ import annotations

import dash
from dash import html

from src.app.logging_setup import get_logger

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/centre.")

dash.register_page(
    __name__,
    path="/stabilite/centre",
    name="Stabilité (centre)",
    title="Stabilité – Centre",
    order=15,
    description="Informations sur le cas 'centre' du diagramme de Poincaré (placeholder).",
)

log.debug("Construction du layout de la page centre...")

layout = html.Div(
    [
        html.Small(
            [
                html.A("Stabilité", href="/stabilite"),
                "  /  ",
                html.Span("Centre"),
            ],
            style={"color": "#666"},
        ),
        html.H2("Centre"),
        html.P(
            "Cas 'centre' : oscillations non amorties (racines imaginaires pures)."
        ),
        html.Ul(
            [
                html.Li("Conditions typiques: tau = 0, delta > 0."),
                html.Li("Racines: lambda = ± i sqrt(delta)."),
                html.Li("Comportement: oscillations persistantes sans amortissement (linéaire idéal)."),
            ]
        ),
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

log.info("Layout de la page centre construit.")

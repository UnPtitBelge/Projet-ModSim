"""
Page de stabilité: mouvement uniforme (tau = 0, delta = 0)

Cette page est enregistrée automatiquement par Dash (multipage natif).
URL sans accents et avec tirets pour cohérence avec la navigation par clic.
Contenu placeholder pour développement futur.
"""

from __future__ import annotations

import dash
from dash import html

from src.app.logging_setup import get_logger

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/mouvement_uniforme.")

dash.register_page(
    __name__,
    path="/stabilite/mouvement_uniforme",
    name="Stabilité (mouvement uniforme)",
    title="Stabilité – Mouvement uniforme",
    order=16,
    description="Informations sur le cas 'mouvement uniforme' du diagramme de Poincaré (placeholder).",
)

log.debug("Construction du layout de la page mouvement uniforme...")

layout = html.Div(
    [
        html.Small(
            [
                html.A("Stabilité", href="/stabilite"),
                "  /  ",
                html.Span("Mouvement uniforme"),
            ],
            style={"color": "#666"},
        ),
        html.H2("Mouvement uniforme"),
        html.P("Cas de mouvement uniforme (τ = 0, Δ = 0)."),
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

log.info("Layout de la page mouvement uniforme construit.")

"""
Page de stabilité: nœud stable dégénéré (discriminant nul, racines réelles égales et négatives)

Cette page est enregistrée automatiquement par Dash (multipage natif).
URL sans accents et avec tirets pour cohérence avec la navigation par clic.
Contenu placeholder pour développement futur.
"""

from __future__ import annotations

import dash
from dash import html

from src.app.logging_setup import get_logger

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/noeud_stable_degenere.")

dash.register_page(
    __name__,
    path="/stabilite/noeud_stable_degenere",
    name="Stabilité (nœud stable dégénéré)",
    title="Stabilité – Nœud stable dégénéré",
    order=17,
    description="Informations sur le cas 'nœud stable dégénéré' du diagramme de Poincaré (placeholder).",
)

log.debug("Construction du layout de la page noeud stable dégénéré...")

layout = html.Div(
    [
        html.Small(
            [
                html.A("Stabilité", href="/stabilite"),
                "  /  ",
                html.Span("Nœud stable dégénéré"),
            ],
            style={"color": "#666"},
        ),
        html.H2("Noeud stable dégénéré"),
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

log.info("Layout de la page noeud stable dégénéré construit.")

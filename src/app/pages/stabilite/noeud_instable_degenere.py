"""
Page de stabilité: nœud instable dégénéré (discriminant nul, racines réelles égales et positives)

Cette page est enregistrée automatiquement par Dash (multipage natif).
URL sans accents et avec tirets pour cohérence avec la navigation par clic.

"""

from __future__ import annotations

import dash
from dash import html

from src.app.logging_setup import get_logger

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/noeud_instable_degenere.")

dash.register_page(
    __name__,
    path="/stabilite/noeud_instable_degenere",
    name="Stabilité (nœud instable dégénéré)",
    title="Stabilité – Nœud instable dégénéré",
    order=18,
    description="Informations sur le cas 'nœud instable dégénéré' du diagramme de Poincaré (placeholder).",
)

log.debug("Construction du layout de la page noeud instable dégénéré...")

layout = html.Div(
    [
        html.Small(
            [
                html.A("Stabilité", href="/stabilite"),
                "  /  ",
                html.Span("Nœud instable dégénéré"),
            ],
            style={"color": "#666"},
        ),
        html.H2("Noeud instable dégénéré"),
        html.P(
            "Cas dégénéré: τ² = 4·Δ avec τ < 0 — deux racines réelles égales positives. Instabilité non oscillatoire."
        ),
        html.Ul(
            [
                html.Li("Conditions typiques: tau < 0, delta = tau^2 / 4."),
                html.Li("Racines: lambda1 = lambda2 = -tau/2 > 0."),
                html.Li("Comportement: instabilité non oscillatoire, réponse de type (C1 + C2·t)·e^{lambda t}."),
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

log.info("Layout de la page noeud instable dégénéré construit.")

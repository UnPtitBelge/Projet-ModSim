"""
Page de stabilité: ligne de points d’équilibre instable

Cette page est enregistrée automatiquement par Dash (multipage natif).
URL sans accents et avec tirets pour cohérence avec la navigation par clic.

"""

from __future__ import annotations

import dash
from dash import html

from src.app.logging_setup import get_logger

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/ligne_pe_instable.")

dash.register_page(
    __name__,
    path="/stabilite/ligne_pe_instable",
    name="Stabilité (ligne de PE instable)",
    title="Stabilité – Ligne de points d’équilibre instable",
    order=20,
    description="Informations sur la ligne de points d’équilibre instable (placeholder).",
)

log.debug("Construction du layout de la page ligne de points d’equilibre instable...")

layout = html.Div(
    [
        html.Small(
            [
                html.A("Stabilité", href="/stabilite"),
                "  /  ",
                html.Span("Ligne de points d’équilibre instable"),
            ],
            style={"color": "#666"},
        ),
        html.H2("Ligne de points d’equilibre instable"),
        html.P(
            "Aperçu des situations présentant un continuum de points d’équilibre instable."
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

log.info("Layout de la page ligne de points d’equilibre instable construit.")

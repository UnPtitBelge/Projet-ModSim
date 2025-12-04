"""
Page de stabilité: nœud stable (tau < 0, 0 < delta < tau^2/4)

Cette page est enregistrée automatiquement par Dash (multipage natif).
URL sans accents et avec tirets pour cohérence avec la navigation par clic.
"""

import dash
from dash import html

from src.app.logging_setup import get_logger

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/noeud_stable.")

dash.register_page(
    __name__,
    path="/stabilite/noeud_stable",
    name="Stabilité (nœud stable)",
    title="Stabilité – Nœud stable",
    order=12,
    description="Informations sur le nœud stable du diagramme de Poincaré.",
)

log.debug("Construction du layout de la page noeud stable...")
layout = html.Div(
    [
        html.Small(
            [
                html.A("Stabilité", href="/stabilite"),
                "  /  ",
                html.Span("Nœud stable"),
            ],
            style={"color": "#666"},
        ),
        html.H2("Nœud stable"),
        html.P(
            "Cette zone correspond aux points situés sous la parabole Δ = τ²/4, mais au-dessus de l’axe x, avec τ < 0."
        ),
        html.H3("Définition géométrique"),
        html.Ul(
            [
                html.Li("tau < 0"),
                html.Li("0 < delta < tau^2 / 4"),
                html.Li("Sous la parabole et à gauche de l’axe vertical τ = 0"),
            ]
        ),
        html.H3("Modèle et racines caractéristiques"),
        html.P(
            "On considère l’équation caractéristique associée: "
            "lambda^2 + tau·lambda + delta = 0."
        ),
        html.Ul(
            [
                html.Li("Racines: lambda = (-tau ± sqrt(tau^2 - 4·delta)) / 2"),
                html.Li("Ici: τ^2 - 4·Δ > 0 ⇒ deux racines réelles distinctes"),
                html.Li("Somme des racines = -τ > 0 (puisque τ < 0)"),
                html.Li("Produit des racines = Δ > 0"),
                html.Li(
                    "Conclusion: les deux racines sont réelles et positives ⇒ instabilité (divergence exponentielle)."
                ),
            ]
        ),
        html.H3("Interprétation stabilité (intermédiaire)"),
        html.Ul(
            [
                html.Li(
                    "Deux racines réelles positives ⇒ combinaison de deux exponentielles croissantes."
                ),
                html.Li(
                    "Réponse divergente, pas d’oscillations (comportement suramorti mais instable)."
                ),
            ]
        ),
        html.H3("Réponse temporelle (forme indicative)"),
        html.P(
            "Pour x'' + τ x' + Δ x = 0, lorsque τ^2 > 4·Δ (nœud), la réponse libre s’écrit:"
        ),
        html.Pre(
            "x(t) = C1 · e^{lambda1 t} + C2 · e^{lambda2 t}",
            style={
                "background": "#f7f7f7",
                "padding": "8px 12px",
                "border": "1px solid #eee",
                "borderRadius": "6px",
                "whiteSpace": "pre-wrap",
            },
        ),
        html.Ul(
            [
                html.Li("λ1, λ2 > 0 (dans cette zone) ⇒ divergence"),
                html.Li("Aucun terme sinus/cosinus: pas d’oscillations"),
            ]
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
log.info("Layout de la page noeud stable construit.")

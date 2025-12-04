"""
Page de stabilité: zone sous l’axe x (Δ < 0)

Cette page est enregistrée automatiquement par Dash (multipage natif).
URL sans accents et avec tirets pour cohérence avec la navigation par clic.
"""

import dash
from dash import html

from src.app.logging_setup import get_logger

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/selle.")

dash.register_page(
    __name__,
    path="/stabilite/selle",
    name="Stabilité (selle)",
    title="Stabilité – Selle",
    order=14,
    description="Informations sur la selle du diagramme de Poincaré.",
)

log.debug("Construction du layout de la page selle...")

layout = html.Div(
    [
        html.Small(
            [
                html.A("Stabilité", href="/stabilite"),
                "  /  ",
                html.Span("Selle"),
            ],
            style={"color": "#666"},
        ),
        html.H2("Selle"),
        html.P(
            "Cette zone correspond aux points situés sous l’axe x, c’est-à-dire Δ < 0."
        ),
        html.H3("Définition géométrique"),
        html.Ul(
            [
                html.Li("delta < 0"),
                html.Li("Toute valeur de τ (aucune contrainte sur τ)"),
                html.Li("Zone strictement sous l’axe horizontal (x)"),
            ]
        ),
        html.H3("Modèle et racines caractéristiques"),
        html.P(
            "On considère l’équation caractéristique associée: "
            "λ^2 + τ·λ + Δ = 0."
        ),
        html.Ul(
            [
                html.Li("Racines: lambda = (-tau ± sqrt(tau^2 - 4·delta)) / 2"),
                html.Li(
                    "Avec Δ < 0 ⇒ τ^2 - 4·Δ = τ^2 + (valeur positive) > 0 ⇒ discriminant strictement positif"
                ),
                html.Li(
                    "Produit des racines = Δ < 0 ⇒ les racines sont réelles et de signes opposés"
                ),
            ]
        ),
        html.H3("Interprétation stabilité (intermédiaire)"),
        html.Ul(
            [
                html.Li(
                    "Présence d’une composante exponentielle croissante (racine positive) et d’une composante décroissante (racine négative)"
                ),
                html.Li("Comportement de type saddle (selle) ⇒ globalement instable"),
                html.Li("Pas d’oscillations: pas de termes sinus/cosinus"),
            ]
        ),
        html.H3("Réponse temporelle (forme indicative)"),
        html.P(
            "Pour x'' + τ x' + Δ x = 0, la réponse libre s’écrit (racines réelles et distinctes):"
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
                html.Li(
                    "λ1 > 0, λ2 < 0 ⇒ terme divergent et terme convergent"
                ),
                html.Li("Absence d’oscillations (pas de composante imaginaire)"),
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

log.info("Layout de la page selle construit.")

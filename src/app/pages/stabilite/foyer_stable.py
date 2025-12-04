"""
Page de stabilité: foyer stable (tau < 0, delta > tau^2/4)

Cette page est enregistrée automatiquement par Dash (multipage natif).
URL sans accents et avec tirets pour cohérence avec la navigation par clic.
"""

import dash
from dash import html

from src.app.logging_setup import get_logger

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/foyer_stable.")

dash.register_page(
    __name__,
    path="/stabilite/foyer_stable",
    name="Stabilité (foyer stable)",
    title="Stabilité – Foyer stable",
    order=10,
    description="Informations sur le foyer stable du diagramme de Poincaré.",
)

log.debug("Construction du layout de la page foyer stable...")

layout = html.Div(
    [
        html.Small(
            [
                html.A("Stabilité", href="/stabilite"),
                "  /  ",
                html.Span("Foyer stable"),
            ],
            style={"color": "#666"},
        ),
        html.H2("Foyer stable"),
        html.P(
            "Cette zone correspond aux points situés au-dessus de la parabole Δ = τ²/4 avec τ < 0."
        ),
        html.H3("Définition géométrique"),
        html.Ul(
            [
                html.Li("tau < 0"),
                html.Li("delta > tau^2 / 4"),
                html.Li("Au-dessus de la parabole, a gauche de l'axe vertical tau = 0"),
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
                html.Li("Partie reelle des racines: Re(lambda) = -tau/2"),
                html.Li(
                    "Dans cette zone: tau < 0 ⇒ Re(lambda) > 0 (partie reelle positive)"
                ),
                html.Li(
                    "Discriminant: tau^2 - 4·delta < 0 ⇒ racines complexes conjuguees"
                ),
            ]
        ),
        html.H3("Interpretation stabilite (intermediaire)"),
        html.Ul(
            [
                html.Li(
                    "Racines complexes avec partie réelle positive ⇒ spirale divergente (instable)."
                ),
                html.Li(
                    "Oscillations dont l’amplitude croît exponentiellement (instabilité oscillatoire)."
                ),
            ]
        ),
        html.H3("Reponse temporelle (forme indicative)"),
        html.P(
            "Pour x'' + τ x' + Δ x = 0, lorsque τ^2 < 4·Δ (foyer), la réponse libre s’écrit:"
        ),
        html.Pre(
            "x(t) = e^{alpha t} [ A cos(omega t) + B sin(omega t) ]",
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
                html.Li("α = -τ/2  (ici: α > 0, croissance)"),
                html.Li(
                    "ω = sqrt(Δ - (τ^2)/4)  (fréquence pseudo-oscillatoire)"
                ),
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

log.info("Layout de la page foyer stable construit.")

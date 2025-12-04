"""
Page de stabilité: foyer instable (tau > 0, delta > tau^2/4)

Cette page est enregistrée automatiquement par Dash (multipage natif).
URL sans accents et avec tirets pour cohérence avec la navigation par clic.
"""

import dash
from dash import html

from src.app.logging_setup import get_logger

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/foyer_instable.")

dash.register_page(
    __name__,
    path="/stabilite/foyer_instable",
    name="Stabilite (foyer instable)",
    title="Stabilite – Foyer instable",
    order=11,
    description="Informations sur le foyer instable du diagramme de Poincaré.",
)
log.debug("Début construction du layout de la page foyer instable...")

layout = html.Div(
    [
        html.Small(
            [
                html.A("Stabilité", href="/stabilite"),
                "  /  ",
                html.Span("Foyer instable"),
            ],
            style={"color": "#666"},
        ),
        html.H2("Foyer instable"),
        html.P(
            "Cette zone correspond aux points situés au-dessus de la parabole Δ = τ²/4 avec τ > 0."
        ),
        html.H3("Définition géométrique"),
        html.Ul(
            [
                html.Li("tau > 0"),
                html.Li("delta > tau^2 / 4"),
                html.Li("Au-dessus de la parabole, a droite de l'axe vertical tau = 0"),
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
                    "Dans cette zone: tau > 0 ⇒ Re(lambda) < 0 (partie reelle negative)"
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
                    "Racines complexes avec partie reelle negative ⇒ spirale convergente (stabilite)."
                ),
                html.Li(
                    "Oscillations dont l'amplitude decroit exponentiellement (oscillations amorties)."
                ),
            ]
        ),
        html.H3("Reponse temporelle (forme indicative)"),
        html.P(
            "Pour x'' + tau x' + delta x = 0, lorsque tau^2 < 4·delta (foyer), la reponse libre s'ecrit:"
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
                html.Li("α = -τ/2  (ici: α < 0, amortissement)"),
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
log.info("Layout de la page foyer instable construit.")

"""
Page de stabilite: zone superieure gauche (tau < 0, delta > tau^2/4)

Cette page est enregistree automatiquement par Dash (multipage natif).
URL sans accents et avec tirets pour coherence avec la navigation par clic.
"""

import dash
from dash import html

from src.app.logging_setup import get_logger

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/zone-superieure-gauche.")

dash.register_page(
    __name__,
    path="/stabilite/zone-superieure-gauche",
    name="Stabilite (sup. gauche)",
    title="Stabilite – Zone superieure gauche",
    order=10,
    description="Informations sur la zone superieure gauche du diagramme de Poincare.",
)

log.debug("Construction du layout de la page zone superieure gauche...")

layout = html.Div(
    [
        html.Small(
            [
                html.A("Stabilite", href="/stabilite"),
                "  /  ",
                html.Span("Zone superieure gauche"),
            ],
            style={"color": "#666"},
        ),
        html.H2("Zone superieure gauche"),
        html.P(
            "Cette zone correspond aux points situes au-dessus de la parabole Δ = τ²/4 avec τ < 0."
        ),
        html.H3("Definition geometrique"),
        html.Ul(
            [
                html.Li("tau < 0"),
                html.Li("delta > tau^2 / 4"),
                html.Li("Au-dessus de la parabole, a gauche de l'axe vertical tau = 0"),
            ]
        ),
        html.H3("Modele et racines caracteristiques"),
        html.P(
            "On considere l'equation caracteristique associee: "
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
                    "Racines complexes avec partie reelle positive ⇒ spirale divergente (instable)."
                ),
                html.Li(
                    "Oscillations dont l'amplitude croit exponentiellement (instabilite oscillatoire)."
                ),
            ]
        ),
        html.H3("Reponse temporelle (forme indicative)"),
        html.P(
            "Pour x'' + tau x' + delta x = 0, lorsque tau^2 < 4·delta (zone superieure), la reponse libre s'ecrit:"
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
                html.Li("alpha = -tau/2  (ici: alpha > 0, croissance)"),
                html.Li(
                    "omega = sqrt(delta - (tau^2)/4)  (frequence pseudo-oscillatoire)"
                ),
            ]
        ),
        html.H3("Exemple numerique (placeholder)"),
        html.Ul(
            [
                html.Li("Choisir tau = -2, delta = 2  ⇒ delta > tau^2/4 = 1"),
                html.Li("alpha = -(-2)/2 = 1 > 0  ⇒ croissance exponentielle"),
                html.Li("omega = sqrt(2 - 1) = 1  ⇒ oscillations a frequence 1 rad/s"),
            ]
        ),
        html.Hr(),
        html.Div(
            [
                html.A("← Retour au sommaire Stabilite", href="/stabilite"),
                html.Span("  |  "),
                html.A("Retour au diagramme de Poincare", href="/poincare"),
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

log.info("Layout de la page zone superieure gauche construit.")

"""
Page de stabilite: zone sous l'axe x (delta < 0)

Cette page est enregistree automatiquement par Dash (multipage natif).
URL sans accents et avec tirets pour coherence avec la navigation par clic.
"""

import dash
from dash import html

from src.app.logging_setup import get_logger

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/zone-sous-axe-x.")

dash.register_page(
    __name__,
    path="/stabilite/zone-sous-axe-x",
    name="Stabilite (sous axe x)",
    title="Stabilite – Zone sous axe x",
    order=14,
    description="Informations sur la zone sous l'axe x du diagramme de Poincare.",
)

log.debug("Construction du layout de la page zone sous axe x...")

layout = html.Div(
    [
        html.Small(
            [
                html.A("Stabilite", href="/stabilite"),
                "  /  ",
                html.Span("Zone sous axe x"),
            ],
            style={"color": "#666"},
        ),
        html.H2("Zone sous axe x"),
        html.P(
            "Cette zone correspond aux points situes sous l'axe x, c'est-a-dire delta < 0."
        ),
        html.H3("Definition geometrique"),
        html.Ul(
            [
                html.Li("delta < 0"),
                html.Li("Toute valeur de tau (aucune contrainte sur tau)"),
                html.Li("Zone strictement sous l'axe horizontal (x)"),
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
                html.Li(
                    "Avec delta < 0 ⇒ tau^2 - 4·delta = tau^2 + (valeur positive) > 0 ⇒ discriminant strictement positif"
                ),
                html.Li(
                    "Produit des racines = delta < 0 ⇒ les racines sont reelles et de signes opposes"
                ),
            ]
        ),
        html.H3("Interpretation stabilite (intermediaire)"),
        html.Ul(
            [
                html.Li(
                    "Presence d'une composante exponentielle croissante (racine positive) et d'une composante decroissante (racine negative)"
                ),
                html.Li("Comportement de type saddle (selle) ⇒ globalement instable"),
                html.Li("Pas d'oscillations: pas de termes sinus/cosinus"),
            ]
        ),
        html.H3("Reponse temporelle (forme indicative)"),
        html.P(
            "Pour x'' + tau x' + delta x = 0, la reponse libre s'ecrit (racines reelles et distinctes):"
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
                    "lambda1 > 0, lambda2 < 0 ⇒ terme divergent et terme convergent"
                ),
                html.Li("Absence d'oscillations (pas de composante imaginaire)"),
            ]
        ),
        html.H3("Exemple numerique (placeholder)"),
        html.Ul(
            [
                html.Li("Choisir tau = 0, delta = -1"),
                html.Li(
                    "Discriminant = 0 - 4·(-1) = 4 ⇒ racines lambda = (0 ± 2)/2 ⇒ {+1, -1}"
                ),
                html.Li(
                    "x(t) = C1 e^{t} + C2 e^{-t} ⇒ instable (croissance exponentielle)"
                ),
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

log.info("Layout de la page zone sous axe x construit.")

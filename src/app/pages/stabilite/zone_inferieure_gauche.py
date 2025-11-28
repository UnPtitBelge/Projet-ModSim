"""
Page de stabilite: zone inferieure gauche (tau < 0, 0 < delta < tau^2/4)

Cette page est enregistree automatiquement par Dash (multipage natif).
URL sans accents et avec tirets pour coherence avec la navigation par clic.
"""

import dash
from dash import html

from src.app.logging_setup import get_logger

log = get_logger(__name__)
log.info("Enregistrement de la page /stabilite/zone-inferieure-gauche.")

dash.register_page(
    __name__,
    path="/stabilite/zone-inferieure-gauche",
    name="Stabilite (inf. gauche)",
    title="Stabilite – Zone inferieure gauche",
    order=12,
    description="Informations sur la zone inferieure gauche du diagramme de Poincare.",
)

log.debug("Construction du layout de la page zone inferieure gauche...")
layout = html.Div(
    [
        html.Small(
            [
                html.A("Stabilite", href="/stabilite"),
                "  /  ",
                html.Span("Zone inferieure gauche"),
            ],
            style={"color": "#666"},
        ),
        html.H2("Zone inferieure gauche"),
        html.P(
            "Cette zone correspond aux points situes sous la parabole Δ = τ²/4, mais au-dessus de l'axe x, avec τ < 0."
        ),
        html.H3("Definition geometrique"),
        html.Ul(
            [
                html.Li("tau < 0"),
                html.Li("0 < delta < tau^2 / 4"),
                html.Li("Sous la parabole et a gauche de l'axe vertical tau = 0"),
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
                html.Li("Ici: tau^2 - 4·delta > 0 ⇒ deux racines reelles distinctes"),
                html.Li("Somme des racines = -tau > 0 (puisque tau < 0)"),
                html.Li("Produit des racines = delta > 0"),
                html.Li(
                    "Conclusion: les deux racines sont reelles et positives ⇒ instabilite (divergence exponentielle)."
                ),
            ]
        ),
        html.H3("Interpretation stabilite (intermediaire)"),
        html.Ul(
            [
                html.Li(
                    "Deux racines reelles positives ⇒ combinaison de deux exponentielles croissantes."
                ),
                html.Li(
                    "Reponse divergent, pas d'oscillations (comportement overdamped mais instable)."
                ),
            ]
        ),
        html.H3("Reponse temporelle (forme indicative)"),
        html.P(
            "Pour x'' + tau x' + delta x = 0, lorsque tau^2 > 4·delta (zone inferieure), la reponse libre s'ecrit:"
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
                html.Li("lambda1, lambda2 > 0 (dans cette zone) ⇒ divergence"),
                html.Li("Aucun terme sinus/cosinus: pas d'oscillations"),
            ]
        ),
        html.H3("Exemple numerique (placeholder)"),
        html.Ul(
            [
                html.Li("Choisir tau = -2, delta = 0.2  ⇒ 0 < delta < tau^2/4 = 1"),
                html.Li(
                    "Racines ≈ (2 ± sqrt(4 - 0.8))/2 = (2 ± sqrt(3.2))/2 ⇒ "
                    "lambda1 ≈ 1.894, lambda2 ≈ 0.106 (toutes deux > 0)"
                ),
                html.Li("Reponse = C1 e^{1.894 t} + C2 e^{0.106 t} (instable)"),
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
log.info("Layout de la page zone inferieure gauche construit.")

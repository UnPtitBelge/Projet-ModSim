"""
Page de sommaire /stabilite pour le diagramme de Poincaré.

Cette page:
- est enregistrée avec le path '/stabilite' (sans accents pour cohérence des URLs)
- fournit un aperçu des différentes zones de stabilité
- propose des liens vers chaque page détaillée déjà existante

Les sous-pages attendues (doivent déjà être présentes):
    /stabilite/foyer_stable
    /stabilite/foyer_instable
    /stabilite/noeud_stable
    /stabilite/noeud_instable
    /stabilite/selle
"""

from __future__ import annotations

import dash
from dash import dcc, html

from src.app.logging_setup import get_logger

log = get_logger(__name__)
log.info("Enregistrement de la page de sommaire /stabilite.")

dash.register_page(
    __name__,
    path="/stabilite",
    name="Stabilite",
    title="Stabilite – Sommaire",
    description="Sommaire des zones de stabilité pour le diagramme de Poincaré.",
    order=2,
)

# Description synthétique de chaque zone (adapté au contenu des pages détaillées)
_ZONES = [
    # Cas basiques (zones principales)
    {
        "label": "Foyer stable",
        "href": "/stabilite/foyer_stable",
        "resume": html.Ul([
            html.Li("$\\tau$ > 0"),
            html.Li("$\\Delta$ > $\\tau^2/4$"),
            html.Li("Racines complexes"),
            html.Li("Partie réelle négative"),
            html.Li("Comportement: stable oscillatoire amorti"),
        ], style={"margin": "4px 0", "paddingLeft": "20px"}),
    },
    {
        "label": "Foyer instable",
        "href": "/stabilite/foyer_instable",
        "resume": html.Ul([
            html.Li("$\\tau$ < 0"),
            html.Li("$\\Delta$ > $\\tau^2/4$"),
            html.Li("Racines complexes"),
            html.Li("Partie réelle positive"),
            html.Li("Comportement: instable oscillatoire"),
        ], style={"margin": "4px 0", "paddingLeft": "20px"}),
    },
    {
        "label": "Noeud stable",
        "href": "/stabilite/noeud_stable",
        "resume": html.Ul([
            html.Li("$\\tau$ > 0"),
            html.Li("0 < $\\Delta$ < $\\tau^2/4$"),
            html.Li("Deux racines réelles négatives"),
            html.Li("Stable non oscillatoire"),
        ], style={"margin": "4px 0", "paddingLeft": "20px"}),
    },
    {
        "label": "Noeud instable",
        "href": "/stabilite/noeud_instable",
        "resume": html.Ul([
            html.Li("$\\tau$ < 0"),
            html.Li("0 < $\\Delta$ < $\\tau^2/4$"),
            html.Li("Deux racines réelles positives"),
            html.Li("Instable non oscillatoire"),
        ], style={"margin": "4px 0", "paddingLeft": "20px"}),
    },
    {
        "label": "Selle",
        "href": "/stabilite/selle",
        "resume": html.Ul([
            html.Li("$\\Delta$ < 0"),
            html.Li("Racines réelles de signes opposés"),
            html.Li("Instabilité mixte"),
            html.Li("Selle"),
        ], style={"margin": "4px 0", "paddingLeft": "20px"}),
    },
    # Cas sur les axes et dégénérés (affichés même si contenus en préparation)
    {
        "label": "Centre",
        "href": "/stabilite/centre",
        "resume": html.Ul([
            html.Li("$\\tau$ = 0"),
            html.Li("$\\Delta$ > 0"),
            html.Li("Racines purement imaginaires"),
            html.Li("Oscillations non amorties"),
        ], style={"margin": "4px 0", "paddingLeft": "20px"}),
    },
    {
        "label": "Mouvement uniforme",
        "href": "/stabilite/mouvement_uniforme",
        "resume": html.Ul([
            html.Li("$\\tau$ = 0"),
            html.Li("$\\Delta$ = 0"),
            html.Li("Racines nulles"),
            html.Li("Mouvement à vitesse constante et solution polynomiale"),
        ], style={"margin": "4px 0", "paddingLeft": "20px"}),
    },
    {
        "label": "Noeud stable dégénéré",
        "href": "/stabilite/noeud_stable_degenere",
        "resume": html.Ul([
            html.Li("$\\tau^2 = 4\\cdot\\Delta$ avec $\\tau$ > 0"),
            html.Li("Racines réelles égales négatives"),
            html.Li("Stabilité = (C1 + C2·t)·e^{λt}"),
        ], style={"margin": "4px 0", "paddingLeft": "20px"}),
    },
    {
        "label": "Noeud instable dégénéré",
        "href": "/stabilite/noeud_instable_degenere",
        "resume": html.Ul([
            html.Li("$\\tau^2 = 4\\cdot\\Delta$ avec $\\tau$ < 0"),
            html.Li("Racines réelles égales positives"),
            html.Li("Instabilité = (C1 + C2·t)·e^{λt}"),
        ], style={"margin": "4px 0", "paddingLeft": "20px"}),
    },
    {
        "label": "Ligne de points d’équilibre stable",
        "href": "/stabilite/ligne_pe_stable",
        "resume": html.Ul([
            html.Li("Continuum de points d’équilibre avec stabilité locale"),
            html.Li("(contenu en préparation)"),
        ], style={"margin": "4px 0", "paddingLeft": "20px"}),
    },
    {
        "label": "Ligne de points d’équilibre instable",
        "href": "/stabilite/ligne_pe_instable",
        "resume": html.Ul([
            html.Li("Continuum de points d’équilibre avec instabilité locale"),
            html.Li("(contenu en préparation)"),
        ], style={"margin": "4px 0", "paddingLeft": "20px"}),
    },
]

layout = html.Div(
    [
        html.H2("Sommaire des zones de stabilite"),
        html.P(
            (
                "Cette page récapitule les différentes régions du diagramme de Poincaré et leur signification "
                "en termes de stabilité des solutions de l'équation caractéristique λ² + τλ + Δ = 0. "
                "Cliquez sur une zone pour afficher la page détaillée correspondante."
            )
        ),
        html.H3("Zones"),
        html.Ul(
            [
                html.Li(
                    html.Div(
                        [
                            html.A(
                                z["label"], href=z["href"], style={"fontWeight": "600"}
                            ),
                            html.Br(),
                            html.Small(z["resume"], style={"color": "#555"}),
                        ],
                        style={"marginBottom": "10px"},
                    )
                )
                for z in _ZONES
            ]
        ),
        html.Hr(),
        html.P(
            (
                "Vous pouvez également accéder à une zone en cliquant directement dessus depuis le diagramme principal "
                "(page d'accueil). La coloration reflète vos interactions."
            ),
            style={"fontSize": "0.9rem", "color": "#444"},
        ),
        html.A(
            "← Retour au diagramme",
            href="/poincare",
            style={"display": "inline-block", "marginTop": "12px"},
        ),
    ],
    style={
        "maxWidth": "900px",
        "padding": "28px 32px",
        "fontFamily": "Arial, sans-serif",
        "lineHeight": "1.5",
        "fontSize": "0.95rem",
    },
)

log.info("Layout de la page /stabilite construit.")

from dash import dcc, html

from src.app.logging_setup import get_logger
from src.app.style.components.layout import app_container, graph_container
from src.app.style.text import TEXT


def build_layout(figure):
    log = get_logger(__name__)
    log.debug("Début construction du layout du diagramme de Poincaré.")
    layout = html.Div(
        [
            html.H2(
                "Analyse et découverte de la notion de stabilité pour des systèmes linéaires continus d'ordre deux",
                style=TEXT["h2"],
            ),
            html.Div(
                [
                    dcc.Graph(
                        id="poincare-graph",
                        figure=figure,
                        style={"height": "70vh"},
                        config={
                            "displaylogo": False,
                            "displayModeBar": False,
                        },
                    )
                ],
                style=graph_container(),
            ),
            html.Div(
                [
                    html.P(
                        (
                            "Ce diagramme de Poincaré illustre différentes zones liées à la stabilité locale "
                            "des systèmes linéaires du second ordre en fonction des paramètres Tau (τ) et Delta (Δ). "
                            "La parabole noire sépare les régions supérieures et inférieures. "
                            "Survolez ou cliquez sur une zone pour la mettre en évidence."
                        ),
                        style=TEXT["p"],
                    ),
                    html.Div(
                        id="output-temp-hover",
                        style={"marginTop": "14px", **TEXT["muted"]},
                    ),
                    html.Div(
                        id="output-temp-click",
                        style={"marginTop": "8px", **TEXT["muted"]},
                    ),
                ],
                style={
                    "maxWidth": "860px",
                },
            ),
        ],
        style={
            **app_container(),
            "padding": "24px",
        },
    )
    log.info("Layout du diagramme de Poincaré construit.")
    return layout


__all__ = ["build_layout"]

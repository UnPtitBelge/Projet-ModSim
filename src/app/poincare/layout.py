"""
Poincaré diagram page layout builder.

This module constructs the layout for the Poincaré diagram interactive page.
The page displays:
1. Title explaining the diagram
2. Interactive graph with hover/click support
3. Description cards with information about regions
4. Output areas for hover and click information

The build_layout() function takes a prepared Plotly figure and wraps it
with styled containers and descriptive text using the design system.
"""

from dash import dcc, html

from src.app.logging_setup import get_logger
from src.app.style.components.layout import (graph_container, section_card,
                                             spacing_section)
from src.app.style.text import TEXT


def build_layout(figure):
    """
    Build the Poincaré diagram page layout.

    Args:
        figure: Plotly graph object with the Poincaré diagram traces and zones

    Returns:
        html.Div containing the complete page structure with title, graph, and descriptions
    """
    log = get_logger(__name__)
    log.debug("Début construction du layout du diagramme de Poincaré.")
    layout = html.Div(
        [
            html.Div(
                [
                    html.H1(
                        "Analyse et découverte des points d'équilibre et de leur stabilité associée dans le diagramme de Poincaré",
                        style=TEXT["h1"],
                    ),
                ],
                style={**section_card(), **spacing_section("bottom")},
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
                    html.H3(
                        "Détail du point d'équilibre sélectionné",
                        style=TEXT["h3"],
                    ),
                    html.Div(
                        "Cliquez sur une zone du diagramme pour afficher la fiche correspondante.",
                        id="poincare-stability-panel",
                        style=TEXT["p"],
                    ),
                ],
                style={**section_card(), **spacing_section("bottom")},
            ),
        ],
    )
    log.info("Layout du diagramme de Poincaré construit.")
    return layout


__all__ = ["build_layout"]

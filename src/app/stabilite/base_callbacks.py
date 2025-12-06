from __future__ import annotations

from typing import Optional

import plotly.graph_objects as go
from dash import Dash, Input, Output, State, html

from .base_layout import stability_ids


def _empty_figure(title: str = "à compléter") -> go.Figure:
    """
    Build a minimal placeholder Plotly figure.
    """
    fig = go.Figure()
    fig.update_layout(
        title=title,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="",
        yaxis_title="",
        template="plotly_white",
    )
    return fig


def register_stability_callbacks(app: Dash, page_key: str) -> None:
    """
    Register minimal callbacks for a stability page.

    Strict nécessaire:
    - Remplit le graphique interactif avec une figure placeholder.
    - Remplit le diagramme de phase avec une figure placeholder.
    - Remplit l’explication pédagogique avec "à compléter".

    Les callbacks peuvent être enrichis ultérieurement avec les données réelles
    (système, points d’équilibre, intégrations, etc.).
    """
    ids = stability_ids(page_key)

    # Graphique interactif (placeholder)
    @app.callback(
        Output(ids["graph"], "figure"),
        Input(ids["graph"], "id"),
        prevent_initial_call=False,
    )
    def _update_interactive_graph(_graph_id: Optional[str]) -> go.Figure:
        # Placeholder minimal
        return _empty_figure("Graphique interactif – à compléter")

    # Diagramme de phase (placeholder)
    @app.callback(
        Output(ids["phase"], "figure"),
        Input(ids["phase"], "id"),
        prevent_initial_call=False,
    )
    def _update_phase_diagram(_phase_id: Optional[str]) -> go.Figure:
        # Placeholder minimal
        return _empty_figure("Diagramme de phase – à compléter")

    # Explication pédagogique (placeholder)
    @app.callback(
        Output(ids["explication"], "children"),
        Input(ids["explication"], "id"),
        State(ids["graph"], "figure"),
        State(ids["phase"], "figure"),
        prevent_initial_call=False,
    )
    def _update_explication(
        _explication_id: Optional[str],
        graph_fig: Optional[go.Figure],
        phase_fig: Optional[go.Figure],
    ):
        # Placeholder strict nécessaire
        return [
            html.P("à compléter"),
        ]

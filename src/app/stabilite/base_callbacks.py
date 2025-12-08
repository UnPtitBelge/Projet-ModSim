from __future__ import annotations

from typing import Optional, Callable

import plotly.graph_objects as go
from dash import Dash, Input, Output, State, html, no_update

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


def register_stability_callbacks(app: Dash, page_key: str, 
                                create_phase_fig: Optional[Callable[[], go.Figure]] = None) -> None:
    """
    Register minimal callbacks for a stability page.
    
    Args:
        app: Dash application
        page_key: Page key for stability page
        create_phase_fig: Optional function to create the phase diagram figure

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

    # Diagramme de phase
    @app.callback(
        Output(ids["phase"], "figure"),
        Input(ids["phase"], "id"),
        prevent_initial_call=False,
    )
    def _update_phase_diagram(_phase_id: Optional[str]) -> go.Figure:
        # Utiliser la fonction personnalisée si fournie, sinon placeholder
        if create_phase_fig is not None:
            return create_phase_fig()
        return _empty_figure("Diagramme de phase – à compléter")

    # Explication pédagogique (placeholder)
    @app.callback(
        Output(ids["explication"], "children"),
        Input(ids["explication"], "id"),
        State(ids["graph"], "figure"),
        State(ids["phase"], "figure"),
        State(ids["explication"], "children"),
        prevent_initial_call=False,
    )
    def _update_explication(
        _explication_id: Optional[str],
        graph_fig: Optional[go.Figure],
        phase_fig: Optional[go.Figure],
        existing_children,
    ):
        # Preserve pre-built pedagogic content when already provided in layout
        if existing_children:
            return no_update

        # Placeholder strict nécessaire si rien n'est fourni
        return [html.P("à compléter")]

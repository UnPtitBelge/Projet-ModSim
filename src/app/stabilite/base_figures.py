from __future__ import annotations

from typing import Iterable, Optional, Tuple

import plotly.graph_objects as go


def _base_placeholder(title: str) -> go.Figure:
    """
    Internal helper: returns a minimal, clean placeholder figure.

    - White template
    - Basic margins
    - Title only
    """
    fig = go.Figure()
    fig.update_layout(
        title=title,
        template="plotly_white",
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig


def interactive_placeholder(
    title: str = "Graphique interactif – à compléter",
) -> go.Figure:
    """
    Strict nécessaire: renvoie une figure placeholder pour le graphique interactif.
    """
    return _base_placeholder(title)


def phase_placeholder(title: str = "Diagramme de phase – à compléter") -> go.Figure:
    """
    Strict nécessaire: renvoie une figure placeholder pour le diagramme de phase.
    """
    return _base_placeholder(title)


def phase_with_equilibria(
    equilibria: Optional[Iterable[Tuple[float, float]]] = None,
    title: str = "Diagramme de phase – à compléter",
) -> go.Figure:
    """
    Optionnel minimal: ajoute des marqueurs de points d'équilibre sur une figure placeholder.
    - `equilibria`: liste optionnelle de coordonnées (x, y) des points d'équilibre.

    Si `equilibria` est vide ou None, renvoie simplement le placeholder de phase.
    """
    fig = phase_placeholder(title)

    points = list(equilibria or [])
    if points:
        xs, ys = zip(*points)
        fig.add_trace(
            go.Scatter(
                x=xs,
                y=ys,
                mode="markers",
                name="Points d'équilibre",
                marker=dict(color="#1f77b4", size=8, symbol="circle"),
            )
        )

    # Axes sobres, sans titres (strict nécessaire)
    fig.update_layout(xaxis_title="", yaxis_title="")
    return fig

"""
Création des graphiques pour la simulation du problème à trois corps.

Génère des animations interactives Plotly montrant l'évolution des trajectoires
des trois corps au fil du temps.
"""

from __future__ import annotations

from typing import Tuple

import numpy as np
import plotly.graph_objs as go

from src.app.chaos.constants import (ANIMATION_FRAME_DURATION,
                                     BODY_MARKER_SIZE, MAX_ANIMATION_FRAMES,
                                     PLOT_AXIS_RANGE, PLOT_BACKGROUND_COLOR,
                                     PLOT_TOTAL_TIME,
                                     TIME_ANNOTATION_BACKGROUND,
                                     TIME_ANNOTATION_BORDER,
                                     TIME_ANNOTATION_FONT_COLOR,
                                     TIME_ANNOTATION_FONT_SIZE,
                                     TRAJECTORY_LINE_WIDTH, TRAJECTORY_OPACITY)
from src.app.chaos.simulation import (Body, create_triangle_bodies,
                                      simulate_three_body_attraction)


def build_three_body_figure_with_data(
    randomize: bool = False,
) -> Tuple[go.Figure, list[Body], np.ndarray, np.ndarray]:
    """
    Crée une animation interactive de la simulation du problème à trois corps.

    Génère une figure Plotly avec animation montrant les trajectoires des trois corps
    soumis à l'attraction gravitationnelle. Chaque corps est représenté par un marqueur
    coloré et sa trajectoire est tracée au fil du temps.

    Args:
        randomize: Active les perturbations aléatoires des positions initiales

    Returns:
        fig: Figure Plotly avec animation
        bodies: Liste des corps avec leurs propriétés initiales
        times: Array des temps de simulation
        positions: Array des positions à chaque instant
    """
    # Créer les corps et exécuter la simulation
    bodies = create_triangle_bodies(
        randomize=randomize,
    )
    masses = [b.mass for b in bodies]

    times, positions = simulate_three_body_attraction(
        total_time=PLOT_TOTAL_TIME,
        masses=masses,
        radii=[b.radius for b in bodies],
        randomize=randomize,
    )

    n_steps = len(times)
    n_bodies = len(bodies)

    # Sous-échantillonnage pour limiter le nombre de frames
    frame_indices = np.linspace(
        0, n_steps - 1, min(MAX_ANIMATION_FRAMES, n_steps), dtype=int
    )

    fig = go.Figure()

    # Créer les traces pour les trajectoires (initialement vides)
    for body in bodies:
        fig.add_trace(
            go.Scatter(
                x=[],
                y=[],
                mode="lines",
                line=dict(color=body.color, width=TRAJECTORY_LINE_WIDTH),
                opacity=TRAJECTORY_OPACITY,
                showlegend=False,
            )
        )

    # Créer les traces pour les marqueurs des corps
    for i, body in enumerate(bodies):
        fig.add_trace(
            go.Scatter(
                x=[positions[0, i, 0]],
                y=[positions[0, i, 1]],
                mode="markers",
                marker=dict(color=body.color, size=BODY_MARKER_SIZE, symbol="circle"),
                showlegend=False,
            )
        )

    # Construire les frames d'animation
    frames = []
    for frame_idx, pos_idx in enumerate(frame_indices):
        frame_data = []
        current_time = times[pos_idx]

        # Ajouter les trajectoires accumulées jusqu'au frame actuel
        for i, body in enumerate(bodies):
            trajectory_x = positions[: pos_idx + 1, i, 0]
            trajectory_y = positions[: pos_idx + 1, i, 1]
            frame_data.append(
                go.Scatter(
                    x=trajectory_x,
                    y=trajectory_y,
                    mode="lines",
                    line=dict(color=body.color, width=TRAJECTORY_LINE_WIDTH),
                    opacity=TRAJECTORY_OPACITY,
                    showlegend=False,
                )
            )

        # Ajouter les positions actuelles des corps
        for i, body in enumerate(bodies):
            frame_data.append(
                go.Scatter(
                    x=[positions[pos_idx, i, 0]],
                    y=[positions[pos_idx, i, 1]],
                    mode="markers",
                    marker=dict(
                        color=body.color, size=BODY_MARKER_SIZE, symbol="circle"
                    ),
                    showlegend=False,
                )
            )

        # Créer le frame avec annotation du temps
        frame = go.Frame(data=frame_data, name=str(frame_idx))
        frame.layout = go.Layout(
            annotations=[
                dict(
                    text=f"t = {current_time:.2f} s",
                    xref="paper",
                    yref="paper",
                    x=0.98,
                    y=0.98,
                    xanchor="right",
                    yanchor="top",
                    showarrow=False,
                    bgcolor=TIME_ANNOTATION_BACKGROUND,
                    bordercolor=TIME_ANNOTATION_BORDER,
                    borderwidth=1,
                    font=dict(
                        color=TIME_ANNOTATION_FONT_COLOR,
                        size=TIME_ANNOTATION_FONT_SIZE,
                    ),
                )
            ]
        )
        frames.append(frame)

    # Configurer le layout de la figure
    axis_range = PLOT_AXIS_RANGE
    fig.update_layout(
        xaxis=dict(
            visible=False,
            showgrid=False,
            zeroline=False,
            scaleanchor="y",
            scaleratio=1,
            range=axis_range,
        ),
        yaxis=dict(
            visible=False,
            showgrid=False,
            zeroline=False,
            range=axis_range,
        ),
        plot_bgcolor=PLOT_BACKGROUND_COLOR,
        paper_bgcolor=PLOT_BACKGROUND_COLOR,
        font=dict(color="#e5e7eb"),
        margin=dict(l=10, r=10, t=20, b=10),
        showlegend=False,
        updatemenus=[
            {
                "type": "buttons",
                "showactive": False,
                "buttons": [
                    {
                        "label": "Lancer",
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "frame": {
                                    "duration": ANIMATION_FRAME_DURATION,
                                    "redraw": True,
                                },
                                "fromcurrent": True,
                                "transition": {"duration": 0},
                                "mode": "immediate",
                            },
                        ],
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [
                            [None],
                            {
                                "frame": {"duration": 0, "redraw": False},
                                "mode": "immediate",
                                "transition": {"duration": 0},
                            },
                        ],
                    },
                    {
                        "label": "Recommencer",
                        "method": "animate",
                        "args": [
                            [0],
                            {
                                "frame": {"duration": 0, "redraw": True},
                                "mode": "immediate",
                                "transition": {"duration": 0},
                                "fromcurrent": False,
                            },
                        ],
                    },
                ],
                "x": 0.0,
                "y": 1.05,
                "direction": "right",
                "pad": {"r": 10, "t": 10},
            }
        ],
    )

    fig.frames = frames

    return fig, bodies, times, positions


def build_three_body_figure() -> go.Figure:
    """
    Crée une figure Plotly avec animation du problème à trois corps.

    Version simplifiée qui retourne uniquement la figure sans les données intermédiaires.

    Returns:
        Figure Plotly avec animation interactive
    """
    fig, _, _, _ = build_three_body_figure_with_data()
    return fig


__all__ = ["build_three_body_figure", "build_three_body_figure_with_data"]

"""
Phase diagram generation for stability analysis visualizations.

This module creates interactive phase portraits showing:
1. System trajectories (solved ODEs)
2. Vector field (direction field with arrows)
3. Equilibrium points
4. Separatrices (for saddles)

Functions generate Plotly figures from system matrices defined by (τ, Δ) coordinates
on the Poincaré diagram. Figures are cached for performance.

System format:
    dx₁/dt = a·x₁ + b·x₂
    dx₂/dt = c·x₁ + d·x₂
"""

from __future__ import annotations

import logging
from typing import Iterable, Optional, Tuple

import numpy as np
import plotly.graph_objects as go
from scipy.integrate import odeint

logger = logging.getLogger(__name__)


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


def _build_phase_diagram_figure(
    a: float,
    b: float,
    c: float,
    d: float,
    title: str = "Diagramme de phase",
) -> go.Figure:
    """
    Internal helper: constructs the phase diagram figure with trajectories and vector field.

    Système: dx₁/dt = a*x₁ + b*x₂
             dx₂/dt = c*x₁ + d*x₂

    Args:
        a, b, c, d: Matrix coefficients
        title: Figure title

    Returns:
        Plotly figure with phase portrait
    """
    fig = go.Figure()

    # Définir le système
    def system(state, t):
        x1_var, x2_var = state
        return [a * x1_var + b * x2_var, c * x1_var + d * x2_var]

    # Générer les conditions initiales espacées de 1.5
    initial_conditions = []
    for x0 in np.arange(-3, 3.5, 1.5):
        for y0 in np.arange(-3, 3.5, 1.5):
            initial_conditions.append((x0, y0))

    # Détecter le type de système
    trace = a + d
    det = a * d - b * c

    # Cas particuliers
    is_centre = trace == 0 and det > 0
    is_mouvement_uniforme = trace == 0 and det == 0
    is_selle = det < 0
    is_unstable = trace > 0 or (det < 0 and trace > 0)

    # Adapter le temps d'intégration
    if is_mouvement_uniforme:
        t = np.linspace(0, 4, 40)
    elif is_selle:
        t = np.linspace(0, 2, 35)
    elif is_centre:
        t = np.linspace(0, 2 * np.pi, 50)
    elif is_unstable:
        t = np.linspace(0, 1.5, 30)
    else:
        t = np.linspace(0, 8, 50)

    # Générer les trajectoires
    x_min, x_max = 0, 0
    y_min, y_max = 0, 0
    trajectories = []

    for x0, y0 in initial_conditions:
        try:
            traj = odeint(system, [x0, y0], t, full_output=False)
            trajectories.append(traj)
            x_min = min(x_min, np.min(traj[:, 0]))
            x_max = max(x_max, np.max(traj[:, 0]))
            y_min = min(y_min, np.min(traj[:, 1]))
            y_max = max(y_max, np.max(traj[:, 1]))
        except:
            pass

    # Ajouter le point d'équilibre
    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers",
            marker=dict(size=10, color="red", symbol="diamond"),
            name="Équilibre",
            hoverinfo="text",
            hovertext="(0, 0)",
            showlegend=True,
        )
    )

    # Calculer les marges
    margin_x = (x_max - x_min) * 0.1 if x_max != x_min else 0.5
    margin_y = (y_max - y_min) * 0.1 if y_max != y_min else 0.5

    # Définir les limites
    x_range = [x_min - margin_x, x_max + margin_x]
    y_range = [y_min - margin_y, y_max + margin_y]

    # Adapter les limites selon le type
    standard_range = 3.6

    if is_mouvement_uniforme:
        x_range = [-5, 5]
        y_range = [-standard_range, standard_range]
    elif is_selle or is_centre or is_unstable:
        x_range = [-standard_range, standard_range]
        y_range = [-standard_range, standard_range]

    # Créer une grille de flèches
    grid_density = 15
    x_arrow_positions = np.linspace(x_range[0], x_range[1], grid_density)
    y_arrow_positions = np.linspace(y_range[0], y_range[1], grid_density)

    # Vectoriser le calcul des normes
    X, Y = np.meshgrid(x_arrow_positions, y_arrow_positions)
    velocities_x = a * X + b * Y
    velocities_y = c * X + d * Y
    norms = np.sqrt(velocities_x**2 + velocities_y**2).flatten()

    valid_norms = norms[norms > 0.01]
    if len(valid_norms) > 0:
        norm_min = np.min(valid_norms)
        norm_max = np.max(valid_norms)
        norm_range = norm_max - norm_min if norm_max != norm_min else 1
    else:
        norm_min, norm_max, norm_range = 0, 1, 1

    norm_min_log = np.log(norm_min + 1)
    norm_max_log = np.log(norm_max + 1)
    norm_range_log = norm_max_log - norm_min_log if norm_max_log != norm_min_log else 1

    # Ajouter les flèches
    for x_pos in x_arrow_positions:
        for y_pos in y_arrow_positions:
            dx = a * x_pos + b * y_pos
            dy = c * x_pos + d * y_pos
            norm = np.sqrt(dx**2 + dy**2)

            if norm > 0.01:
                dx_norm = dx / norm
                dy_norm = dy / norm

                norm_log = np.log(norm + 1)
                intensity_normalized = (
                    (norm_log - norm_min_log) / norm_range_log
                    if norm_range_log > 0
                    else 0.5
                )
                intensity_normalized = np.clip(intensity_normalized, 0, 1)
                intensity_amplified = intensity_normalized**0.5

                offset = 0.2 + intensity_amplified * 0.4

                x_tail = x_pos - dx_norm * offset
                y_tail = y_pos - dy_norm * offset
                angle = np.arctan2(dy_norm, dx_norm)

                # Ajouter la tige
                fig.add_trace(
                    go.Scatter(
                        x=[x_tail, x_pos],
                        y=[y_tail, y_pos],
                        mode="lines",
                        line=dict(color="#1f77b4", width=1),
                        hoverinfo="skip",
                        showlegend=False,
                    )
                )

                # Ajouter la tête
                head_angle = np.pi / 6
                head_length = 0.15

                angle_left = angle + head_angle
                angle_right = angle - head_angle

                p1_x = x_pos - head_length * np.cos(angle_left)
                p1_y = y_pos - head_length * np.sin(angle_left)
                p2_x = x_pos - head_length * np.cos(angle_right)
                p2_y = y_pos - head_length * np.sin(angle_right)

                fig.add_trace(
                    go.Scatter(
                        x=[x_pos, p1_x],
                        y=[y_pos, p1_y],
                        mode="lines",
                        line=dict(color="#1f77b4", width=1.5),
                        hoverinfo="skip",
                        showlegend=False,
                    )
                )

                fig.add_trace(
                    go.Scatter(
                        x=[x_pos, p2_x],
                        y=[y_pos, p2_y],
                        mode="lines",
                        line=dict(color="#1f77b4", width=1.5),
                        hoverinfo="skip",
                        showlegend=False,
                    )
                )

    # Configurer le layout
    fig.update_layout(
        title=title,
        xaxis_title="x₁",
        yaxis_title="x₂",
        hovermode="closest",
        width=None,
        height=500,
        xaxis=dict(range=x_range, scaleanchor="y", scaleratio=1),
        yaxis=dict(range=y_range, scaleanchor="x", scaleratio=1),
        template="plotly_white",
    )

    return fig


def create_phase_diagram(
    a: float, b: float, c: float, d: float, title: str = "Diagramme de phase"
) -> go.Figure:
    """
    Crée un diagramme de phase pour un système 2D linéaire.

    Système: dx₁/dt = a*x₁ + b*x₂
             dx₂/dt = c*x₁ + d*x₂

    Args:
        a, b, c, d: Paramètres de la matrice Jacobienne
        title: Titre du diagramme

    Returns:
        Figure Plotly avec trajectoires et champ vectoriel
    """
    return _build_phase_diagram_figure(a, b, c, d, title)


def create_system_graph(
    a: float,
    b: float,
    c: float,
    d: float,
    initial_condition: Tuple[float, float] = (1.0, 0.5),
    title: str = "Évolution temporelle du système",
) -> go.Figure:
    """
    Crée un graphe montrant l'évolution temporelle d'une trajectoire du système.

    Système: dx₁/dt = a*x₁ + b*x₂
             dx₂/dt = c*x₁ + d*x₂

    Args:
        a, b, c, d: Paramètres de la matrice Jacobienne
        initial_condition: Conditions initiales (x₁₀, x₂₀)
        title: Titre du graphe

    Returns:
        Figure Plotly avec x₁(t) et x₂(t)
    """
    fig = go.Figure()

    # Définir le système
    def system(state, t):
        x1_var, x2_var = state
        return [a * x1_var + b * x2_var, c * x1_var + d * x2_var]

    # Détecter le type de système pour adapter le temps d'intégration
    trace = a + d
    det = a * d - b * c

    is_centre = trace == 0 and det > 0
    is_mouvement_uniforme = trace == 0 and det == 0
    is_selle = det < 0
    is_unstable = trace > 0 or (det < 0 and trace > 0)

    # Adapter le temps d'intégration
    if is_mouvement_uniforme:
        t = np.linspace(0, 8, 400)
    elif is_selle:
        t = np.linspace(0, 4, 300)
    elif is_centre:
        t = np.linspace(0, 4 * np.pi, 400)
    elif is_unstable:
        t = np.linspace(0, 3, 200)
    else:
        t = np.linspace(0, 16, 400)

    # Résoudre le système
    try:
        trajectory = odeint(system, list(initial_condition), t, full_output=False)
        x1_vals = trajectory[:, 0]
        x2_vals = trajectory[:, 1]
    except:
        # Retourner un placeholder en cas d'erreur
        fig.update_layout(title=title, template="plotly_white")
        return fig

    # Ajouter les courbes x₁(t) et x₂(t)
    fig.add_trace(
        go.Scatter(
            x=t,
            y=x1_vals,
            mode="lines",
            name="x₁(t)",
            line=dict(color="#EA580C", width=2),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=t,
            y=x2_vals,
            mode="lines",
            name="x₂(t)",
            line=dict(color="#0066CC", width=2),
        )
    )

    # Configuration du layout
    fig.update_layout(
        title=title,
        xaxis_title="Temps (t)",
        yaxis_title="Valeur",
        hovermode="x unified",
        width=None,
        height=500,
        template="plotly_white",
        legend=dict(x=0.02, y=0.98),
    )

    return fig

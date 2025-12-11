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
    Constructs phase portrait following the qualitative analysis recipe:
    1. Calculate trace and determinant
    2. Predict equilibrium nature (from Poincaré diagram)
    3. Calculate eigenvalues
    4. Determine eigenvectors and plot invariant lines
    5. Calculate isoclines (dx₁/dt=0 and dx₂/dt=0)
    6. Analyze derivative signs in regions
    7. Draw velocity vectors at chosen points
    8. Plot trajectories respecting asymptotic directions

    Système: dx₁/dt = a*x₁ + b*x₂
             dx₂/dt = c*x₁ + d*x₂

    Args:
        a, b, c, d: Matrix coefficients
        title: Figure title

    Returns:
        Plotly figure with complete phase portrait
    """
    fig = go.Figure()

    # === ÉTAPE 1: Calculer trace et déterminant ===
    trace = a + d
    det = a * d - b * c

    # === ÉTAPE 2: Prédire la nature de l'équilibre ===
    discriminant = trace**2 - 4 * det
    is_centre = abs(trace) < 1e-10 and det > 0
    is_mouvement_uniforme = abs(trace) < 1e-10 and abs(det) < 1e-10
    is_selle = det < 0
    is_unstable = trace > 0

    # === ÉTAPE 3: Calculer les valeurs propres ===
    if abs(discriminant) < 1e-10:
        # Valeur propre double
        lambda1 = lambda2 = trace / 2
        eigenvalues_real = True
    elif discriminant > 0:
        # Valeurs propres réelles distinctes
        lambda1 = (trace + np.sqrt(discriminant)) / 2
        lambda2 = (trace - np.sqrt(discriminant)) / 2
        eigenvalues_real = True
    else:
        # Valeurs propres complexes conjuguées
        real_part = trace / 2
        imag_part = np.sqrt(-discriminant) / 2
        lambda1 = complex(real_part, imag_part)
        lambda2 = complex(real_part, -imag_part)
        eigenvalues_real = False

    # Définir les limites du graphique
    standard_range = 3.6
    if is_mouvement_uniforme:
        x_range = [-5, 5]
        y_range = [-standard_range, standard_range]
    else:
        x_range = [-standard_range, standard_range]
        y_range = [-standard_range, standard_range]

    # === ÉTAPE 4: Vecteurs propres et droites invariantes ===
    if eigenvalues_real and not is_mouvement_uniforme:
        # Calculer les vecteurs propres pour valeurs propres réelles
        eigenvectors = []
        for lam in [lambda1, lambda2]:
            if abs(lam) > 1e-10 or abs(a - lam) > 1e-10:
                # Vecteur propre: (A - λI)v = 0
                # Pour λ₁: (a-λ)v₁ + b*v₂ = 0
                if abs(b) > 1e-10:
                    v = np.array([b, lam - a])
                elif abs(c) > 1e-10:
                    v = np.array([lam - d, c])
                else:
                    v = np.array([1, 0]) if abs(a - lam) < 1e-10 else np.array([0, 1])

                # Normaliser
                v = v / np.linalg.norm(v) if np.linalg.norm(v) > 0 else v
                eigenvectors.append(v)

        # Tracer les droites invariantes (directions propres)
        for i, v in enumerate(eigenvectors):
            if np.linalg.norm(v) > 1e-10:
                # Prolonger la ligne sur toute la plage
                t_line = np.linspace(-6, 6, 100)
                x_line = t_line * v[0]
                y_line = t_line * v[1]

                # Filtrer pour rester dans les limites
                mask = (
                    (x_line >= x_range[0])
                    & (x_line <= x_range[1])
                    & (y_line >= y_range[0])
                    & (y_line <= y_range[1])
                )

                if np.any(mask):
                    fig.add_trace(
                        go.Scatter(
                            x=x_line[mask],
                            y=y_line[mask],
                            mode="lines",
                            line=dict(color="purple", width=2, dash="dash"),
                            name=f"Direction propre {i+1}",
                            hoverinfo="skip",
                            showlegend=(i == 0),
                            legendgroup="eigenvectors",
                        )
                    )

    # === ÉTAPE 5: Calculer les isoclines ===
    # Isocline dx₁/dt = 0: a*x₁ + b*x₂ = 0 => x₂ = -(a/b)*x₁ (si b≠0)
    # Isocline dx₂/dt = 0: c*x₁ + d*x₂ = 0 => x₂ = -(c/d)*x₁ (si d≠0)

    if abs(b) > 1e-10:
        x_iso1 = np.linspace(x_range[0], x_range[1], 100)
        y_iso1 = -(a / b) * x_iso1
        mask1 = (y_iso1 >= y_range[0]) & (y_iso1 <= y_range[1])
        if np.any(mask1):
            fig.add_trace(
                go.Scatter(
                    x=x_iso1[mask1],
                    y=y_iso1[mask1],
                    mode="lines",
                    line=dict(color="orange", width=1.5, dash="dot"),
                    name="Isocline dx₁/dt=0",
                    hoverinfo="skip",
                    showlegend=True,
                )
            )

    if abs(d) > 1e-10:
        x_iso2 = np.linspace(x_range[0], x_range[1], 100)
        y_iso2 = -(c / d) * x_iso2
        mask2 = (y_iso2 >= y_range[0]) & (y_iso2 <= y_range[1])
        if np.any(mask2):
            fig.add_trace(
                go.Scatter(
                    x=x_iso2[mask2],
                    y=y_iso2[mask2],
                    mode="lines",
                    line=dict(color="green", width=1.5, dash="dot"),
                    name="Isocline dx₂/dt=0",
                    hoverinfo="skip",
                    showlegend=True,
                )
            )

    # === ÉTAPE 7: Dessiner des vecteurs vitesse ===
    grid_density = 12
    x_arrow = np.linspace(x_range[0], x_range[1], grid_density)
    y_arrow = np.linspace(y_range[0], y_range[1], grid_density)

    for x_pos in x_arrow:
        for y_pos in y_arrow:
            dx = a * x_pos + b * y_pos
            dy = c * x_pos + d * y_pos
            norm = np.sqrt(dx**2 + dy**2)

            if norm > 0.05:
                # Normaliser et mettre à l'échelle
                scale = 0.25
                dx_scaled = (dx / norm) * scale
                dy_scaled = (dy / norm) * scale

                fig.add_trace(
                    go.Scatter(
                        x=[x_pos, x_pos + dx_scaled],
                        y=[y_pos, y_pos + dy_scaled],
                        mode="lines",
                        line=dict(color="rgba(31, 119, 180, 0.5)", width=1.5),
                        hoverinfo="skip",
                        showlegend=False,
                    )
                )

                # Ajouter une petite tête de flèche
                angle = np.arctan2(dy, dx)
                head_len = 0.08
                head_ang = np.pi / 6

                x_tip = x_pos + dx_scaled
                y_tip = y_pos + dy_scaled

                x_head1 = x_tip - head_len * np.cos(angle - head_ang)
                y_head1 = y_tip - head_len * np.sin(angle - head_ang)
                x_head2 = x_tip - head_len * np.cos(angle + head_ang)
                y_head2 = y_tip - head_len * np.sin(angle + head_ang)

                fig.add_trace(
                    go.Scatter(
                        x=[x_tip, x_head1],
                        y=[y_tip, y_head1],
                        mode="lines",
                        line=dict(color="rgba(31, 119, 180, 0.5)", width=1.5),
                        hoverinfo="skip",
                        showlegend=False,
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=[x_tip, x_head2],
                        y=[y_tip, y_head2],
                        mode="lines",
                        line=dict(color="rgba(31, 119, 180, 0.5)", width=1.5),
                        hoverinfo="skip",
                        showlegend=False,
                    )
                )

    # === ÉTAPE 8: Tracer les trajectoires ===
    def system(state, t):
        x1_var, x2_var = state
        return [a * x1_var + b * x2_var, c * x1_var + d * x2_var]

    # Adapter le temps d'intégration selon le type
    if is_mouvement_uniforme:
        t_span = np.linspace(0, 4, 40)
    elif is_selle:
        t_span = np.linspace(0, 2, 35)
    elif is_centre:
        t_span = np.linspace(0, 2 * np.pi, 50)
    elif is_unstable:
        t_span = np.linspace(0, 1.5, 30)
    else:
        t_span = np.linspace(0, 8, 50)

    # Conditions initiales bien choisies
    initial_conditions = []
    for x0 in np.arange(-3, 3.5, 1.2):
        for y0 in np.arange(-3, 3.5, 1.2):
            if abs(x0) > 0.3 or abs(y0) > 0.3:  # Éviter l'origine
                initial_conditions.append((x0, y0))

    # Tracer les trajectoires
    for x0, y0 in initial_conditions:
        try:
            traj = odeint(system, [x0, y0], t_span, full_output=False)
            x_traj = traj[:, 0]
            y_traj = traj[:, 1]

            # Filtrer les points dans les limites
            mask = (
                (x_traj >= x_range[0] - 1)
                & (x_traj <= x_range[1] + 1)
                & (y_traj >= y_range[0] - 1)
                & (y_traj <= y_range[1] + 1)
            )

            if np.any(mask):
                fig.add_trace(
                    go.Scatter(
                        x=x_traj[mask],
                        y=y_traj[mask],
                        mode="lines",
                        line=dict(color="rgba(100, 100, 100, 0.4)", width=1),
                        hoverinfo="skip",
                        showlegend=False,
                    )
                )
        except:
            pass

    # === Ajouter le point d'équilibre ===
    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers",
            marker=dict(size=10, color="red", symbol="diamond"),
            name="Point d'équilibre",
            hoverinfo="text",
            hovertext="(0, 0)",
            showlegend=True,
        )
    )

    # === Configuration finale ===
    fig.update_layout(
        title=title,
        xaxis_title="x₁",
        yaxis_title="x₂",
        hovermode="closest",
        width=None,
        height=500,
        xaxis=dict(
            range=x_range,
            scaleanchor="y",
            scaleratio=1,
            gridcolor="#E5E7EB",
        ),
        yaxis=dict(
            range=y_range,
            scaleanchor="x",
            scaleratio=1,
            gridcolor="#E5E7EB",
        ),
        template="plotly_white",
        showlegend=False,  # Désactiver la légende Plotly (sera dans le HTML)
        margin=dict(l=60, r=60, t=60, b=60),
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
        xaxis=dict(gridcolor="#E5E7EB"),
        yaxis=dict(gridcolor="#E5E7EB"),
        legend=dict(
            x=0.02,
            y=0.98,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="#E5E7EB",
            borderwidth=1,
        ),
        margin=dict(l=60, r=60, t=60, b=60),
    )

    return fig

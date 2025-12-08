"""
Utilities for eigenvalue calculations and visualizations.
"""

from __future__ import annotations

from typing import Dict, Tuple

import numpy as np
import plotly.graph_objects as go

from src.app.style.palette import PALETTE
from src.app.style.plot.theme import FIGURE_THEME, apply_to_figure


def tau_delta_to_matrix(tau: float, delta: float) -> Tuple[float, float, float, float]:
    """
    Convert tau (trace) and delta (determinant) to matrix coefficients (a, b, c, d).

    For a system matrix:
    [ a  b ]
    [ c  d ]

    We have:
    - τ = a + d (trace)
    - Δ = ad - bc (determinant)

    To maintain the same eigenvalues while allowing exploration, we use:
    - a = τ/2 + small offset
    - d = τ/2 - small offset
    - b = 1 (arbitrary choice for coupling)
    - c = (ad - Δ) / b

    This ensures: trace = a+d = τ and det = ad-bc = Δ

    Args:
        tau: Trace of the system matrix
        delta: Determinant of the system matrix

    Returns:
        Tuple (a, b, c, d) representing the matrix coefficients
    """
    # Choose b = 1 for simplicity (could be any non-zero value)
    b = 1.0

    # Split trace equally with small offset for variation
    offset = 0.1
    a = tau / 2 + offset
    d = tau / 2 - offset

    # Calculate c from determinant equation: Δ = ad - bc
    # Therefore: c = (ad - Δ) / b
    c = (a * d - delta) / b

    return a, b, c, d


def tau_delta_to_matrix_typed(
    tau: float, delta: float, equilibrium_type: str
) -> Tuple[float, float, float, float]:
    """
    Convert tau and delta to matrix coefficients that respect the equilibrium type structure.

    Args:
        tau: Trace of the system matrix
        delta: Determinant of the system matrix
        equilibrium_type: Type of equilibrium point

    Returns:
        Tuple (a, b, c, d) representing the matrix coefficients
    """
    eq_type = equilibrium_type.lower()

    # Foyers (stable/instable): structure spirale
    if "foyer" in eq_type:
        # Structure: [ -α   β ]
        #            [ -β  -α ]
        # τ = -2α, Δ = α² + β²
        alpha = -tau / 2
        beta_squared = delta - alpha**2
        beta = beta_squared**0.5 if beta_squared > 0 else 0.5
        return (-alpha, beta, -beta, -alpha)

    # Nœuds (stable/instable/dégénéré): structure diagonale ou quasi-diagonale
    elif "noeud" in eq_type or "n\u0153ud" in eq_type:
        # Structure diagonale ou proche
        # [ λ1   0  ]  ou  [ λ1   ε ]
        # [  0  λ2 ]       [  0  λ2 ]
        lambda1, lambda2 = calculate_eigenvalues(tau, delta)
        eps = (
            0.1
            if "degenere" not in eq_type
            and "d\u00e9g\u00e9n\u00e9r\u00e9" not in eq_type
            else 0
        )
        return (lambda1.real, eps, 0, lambda2.real)

    # Centre: structure antisymétrique
    elif "centre" in eq_type:
        # Structure: [  0   β ]
        #            [ -β   0 ]
        # τ = 0, Δ = β²
        beta = delta**0.5 if delta > 0 else 1.0
        return (0, beta, -beta, 0)

    # Selle: une valeur propre positive, une négative
    elif "selle" in eq_type:
        # Structure: [ λ1   0 ]  where λ1 > 0, λ2 < 0
        #            [  0  λ2 ]
        lambda1, lambda2 = calculate_eigenvalues(tau, delta)
        return (lambda1.real, 0.5, 0.5, lambda2.real)

    # Mouvement uniforme: structure où une variable ne varie pas
    elif "mouvement" in eq_type or "uniforme" in eq_type:
        # Structure: [  0   1 ]  (ou similaire)
        #            [  0   0 ]
        # Représente: dx₁/dt = x₂, dx₂/dt = 0
        # Une valeur propre nulle (pas d'accélération)
        return (0, 1, 0, 0)

    # Ligne de points d'équilibre
    elif "ligne" in eq_type:
        # Une valeur propre nulle, une non-nulle
        # [ λ   0 ]
        # [ 0   0 ]
        lambda_val = tau  # La seule valeur propre non-nulle
        return (lambda_val, 0.1, 0, 0)

    # Par défaut: utiliser la méthode générique
    else:
        return tau_delta_to_matrix(tau, delta)


def calculate_eigenvalues(tau: float, delta: float) -> Tuple[complex, complex]:
    """
    Calculate eigenvalues from tau (trace) and delta (determinant).

    For characteristic equation: λ² - τλ + Δ = 0
    Solution: λ = (τ ± √(τ² - 4Δ)) / 2

    Args:
        tau: Trace of the system matrix
        delta: Determinant of the system matrix

    Returns:
        Tuple of two eigenvalues (may be complex)
    """
    discriminant = tau**2 - 4 * delta

    if discriminant >= 0:
        # Real eigenvalues
        sqrt_disc = np.sqrt(discriminant)
        lambda1 = (tau + sqrt_disc) / 2
        lambda2 = (tau - sqrt_disc) / 2
    else:
        # Complex eigenvalues
        sqrt_disc = np.sqrt(-discriminant) * 1j
        lambda1 = (tau + sqrt_disc) / 2
        lambda2 = (tau - sqrt_disc) / 2

    return lambda1, lambda2


def classify_equilibrium(tau: float, delta: float) -> str:
    """
    Classify equilibrium point type based on tau and delta.

    Args:
        tau: Trace of the system matrix
        delta: Determinant of the system matrix

    Returns:
        String describing the equilibrium type
    """
    discriminant = tau**2 - 4 * delta

    # Special cases
    if abs(tau) < 1e-10 and abs(delta) < 1e-10:
        return "Mouvement uniforme"

    if abs(tau) < 1e-10:
        if delta > 0:
            return "Centre"
        else:
            return "Ligne de points d'équilibre"

    if delta < 0:
        return "Point selle (instable)"

    # Parabola: τ² = 4Δ
    if abs(discriminant) < 1e-10:
        if tau > 0:
            return "Nœud dégénéré stable"
        else:
            return "Nœud dégénéré instable"

    # Above parabola: complex eigenvalues
    if discriminant < 0:
        if tau > 0:
            return "Foyer stable"
        else:
            return "Foyer instable"

    # Below parabola: real eigenvalues
    if tau > 0:
        return "Nœud stable"
    else:
        return "Nœud instable"


def create_eigenvalue_plot(tau: float, delta: float) -> go.Figure:
    """
    Create a plot showing the eigenvalues in the complex plane.

    Args:
        tau: Current trace value
        delta: Current determinant value

    Returns:
        Plotly figure showing eigenvalues
    """
    lambda1, lambda2 = calculate_eigenvalues(tau, delta)

    fig = go.Figure()

    # Add eigenvalues as scatter points
    fig.add_trace(
        go.Scatter(
            x=[lambda1.real, lambda2.real],
            y=[lambda1.imag, lambda2.imag],
            mode="markers",
            marker=dict(
                size=15,
                color=PALETTE.primary,
                line=dict(width=2, color=PALETTE.surface),
            ),
            name="Valeurs propres",
            text=[f"λ₁ = {lambda1:.3f}", f"λ₂ = {lambda2:.3f}"],
            hovertemplate="%{text}<extra></extra>",
        )
    )

    # Add axes
    max_range = (
        max(
            abs(lambda1.real),
            abs(lambda1.imag),
            abs(lambda2.real),
            abs(lambda2.imag),
            1,
        )
        * 1.2
    )

    fig.add_shape(
        type="line",
        x0=-max_range,
        x1=max_range,
        y0=0,
        y1=0,
        line=dict(color=PALETTE.text_muted, width=1, dash="dash"),
    )

    fig.add_shape(
        type="line",
        x0=0,
        x1=0,
        y0=-max_range,
        y1=max_range,
        line=dict(color=PALETTE.text_muted, width=1, dash="dash"),
    )

    # Stability region (left half-plane)
    fig.add_shape(
        type="rect",
        x0=-max_range,
        x1=0,
        y0=-max_range,
        y1=max_range,
        fillcolor=PALETTE.zone_lower_left,
        line=dict(width=0),
        layer="below",
    )

    fig.update_layout(
        xaxis_title="Partie réelle",
        yaxis_title="Partie imaginaire",
        xaxis=dict(
            range=[-max_range, max_range],
            zeroline=False,
            gridcolor=PALETTE.border,
        ),
        yaxis=dict(
            range=[-max_range, max_range],
            zeroline=False,
            gridcolor=PALETTE.border,
            scaleanchor="x",
            scaleratio=1,
        ),
        hovermode="closest",
        showlegend=False,
    )

    apply_to_figure(fig)

    return fig


def format_eigenvalue_display(tau: float, delta: float) -> Dict:
    """
    Format eigenvalue information for display.

    Args:
        tau: Trace value
        delta: Determinant value

    Returns:
        Dictionary with formatted eigenvalue information
    """
    lambda1, lambda2 = calculate_eigenvalues(tau, delta)
    eq_type = classify_equilibrium(tau, delta)

    # Format eigenvalues
    if abs(lambda1.imag) < 1e-10:
        # Real eigenvalues
        lambda1_str = f"{lambda1.real:.4f}"
        lambda2_str = f"{lambda2.real:.4f}"
        nature = "Valeurs propres réelles"
    else:
        # Complex eigenvalues
        real_part = lambda1.real
        imag_part = abs(lambda1.imag)
        lambda1_str = f"{real_part:.4f} + {imag_part:.4f}i"
        lambda2_str = f"{real_part:.4f} - {imag_part:.4f}i"
        nature = "Valeurs propres complexes conjuguées"

    # Stability
    if lambda1.real < -1e-10 and lambda2.real < -1e-10:
        stability = "Stable"
        stability_color = PALETTE.secondary
    elif lambda1.real > 1e-10 or lambda2.real > 1e-10:
        stability = "Instable"
        stability_color = PALETTE.accent_red
    else:
        stability = "Marginalement stable"
        stability_color = PALETTE.accent_amber

    return {
        "lambda1": lambda1_str,
        "lambda2": lambda2_str,
        "eigenvalues": f"λ₁ = {lambda1_str}, λ₂ = {lambda2_str}",
        "nature": nature,
        "type": eq_type,
        "stability": stability,
        "stability_color": stability_color,
    }

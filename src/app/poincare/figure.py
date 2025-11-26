"""
Construit la figure Plotly du diagramme de Poincaré.

Trace indices:
0  parabole
1–5 zones de stabilité (polygones remplis)

API principale: build_poincare_figure(config=None) -> plotly.graph_objs.Figure
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import plotly.graph_objs as go

from .constants import DELTA_MAX, N_SAMPLES, TAU_MAX, TAU_MIN


@dataclass(frozen=True)
class PoincareConfig:
    tau_min: float = TAU_MIN
    tau_max: float = TAU_MAX
    samples: int = N_SAMPLES  # number of tau discretization points
    # Base colors (rgba for transparency to preserve axis visibility)
    base_color: str = "rgba(210, 70, 70, 0.35)"
    hover_color: str = "rgba(240, 150, 150, 0.55)"
    click_color: str = "rgba(150, 30, 30, 0.65)"
    parabola_line_color: str = "black"
    parabola_line_width: int = 4
    title: str = "Diagramme de Poincaré"
    x_label: str = "Tau"
    y_label: str = "Delta"


def _generate_core_arrays(cfg: PoincareConfig):
    """
    Generate tau axis and parabola values.

    Returns
    -------
    tau_vals : np.ndarray
    parabola_vals : np.ndarray
    """
    tau_vals = np.linspace(cfg.tau_min, cfg.tau_max, cfg.samples)
    parabola_vals = (tau_vals**2) / 4.0
    return tau_vals, parabola_vals


def _build_polygons(tau_vals: np.ndarray, parabola_vals: np.ndarray):
    """
    Construct polygon coordinate pairs for each zone.

    Returns
    -------
    dict[str, tuple[np.ndarray, np.ndarray]]
        Keys: upper_left, upper_right, lower_left, lower_right, lower
        Each value: (x_coords, y_coords)
    """
    left_mask = tau_vals < 0
    right_mask = tau_vals > 0

    parabola_left = parabola_vals[left_mask]
    parabola_right = parabola_vals[right_mask]

    # Upper Left: between parabola and DELTA_MAX for tau < 0
    UL_x = np.concatenate([tau_vals[left_mask], tau_vals[left_mask][::-1]])
    UL_y = np.concatenate([parabola_left, [DELTA_MAX] * len(parabola_left)])

    # Upper Right: tau > 0
    UR_x = np.concatenate([tau_vals[right_mask], tau_vals[right_mask][::-1]])
    UR_y = np.concatenate([parabola_right, [DELTA_MAX] * len(parabola_right)])

    # Lower Left: between parabola and 0 for tau < 0
    LL_x = np.concatenate([tau_vals[left_mask], tau_vals[left_mask][::-1]])
    LL_y = np.concatenate([parabola_left, [0] * len(parabola_left)])

    # Lower Right: between parabola and 0 for tau > 0
    LR_x = np.concatenate([tau_vals[right_mask], tau_vals[right_mask][::-1]])
    LR_y = np.concatenate([parabola_right, [0] * len(parabola_right)])

    # Lower Zone: between 0 and -DELTA_MAX for all tau
    LOW_x = np.concatenate([tau_vals, tau_vals[::-1]])
    LOW_y = np.concatenate([[0] * len(tau_vals), [-DELTA_MAX] * len(tau_vals)])

    return {
        "upper_left": (UL_x, UL_y),
        "upper_right": (UR_x, UR_y),
        "lower_left": (LL_x, LL_y),
        "lower_right": (LR_x, LR_y),
        "lower": (LOW_x, LOW_y),
    }


def build_poincare_figure(config: PoincareConfig | None = None) -> go.Figure:
    """
    Build and return the base Poincaré diagram figure.

    Parameters
    ----------
    config : PoincareConfig | None
        Optional configuration. If None, defaults are used.

    Returns
    -------
    plotly.graph_objs.Figure
    """
    cfg = config or PoincareConfig()
    tau_vals, parabola_vals = _generate_core_arrays(cfg)
    polygons = _build_polygons(tau_vals, parabola_vals)

    fig = go.Figure()

    # Parabola line (curve index 0)
    fig.add_trace(
        go.Scatter(
            x=tau_vals,
            y=parabola_vals,
            mode="lines",
            line=dict(color=cfg.parabola_line_color, width=cfg.parabola_line_width),
            name="Parabola",
        )
    )

    def add_zone(name: str, coords: tuple[np.ndarray, np.ndarray]):
        x, y = coords
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                fill="toself",
                fillcolor=cfg.base_color,
                line=dict(width=0),
                name=name,
                hoverinfo="none",  # we rely on curveNumber-based identification
            )
        )

    # Order matters for callbacks referencing curveNumber
    add_zone("Upper Left Zone", polygons["upper_left"])
    add_zone("Upper Right Zone", polygons["upper_right"])
    add_zone("Lower Left Zone", polygons["lower_left"])
    add_zone("Lower Right Zone", polygons["lower_right"])
    add_zone("Lower Zone", polygons["lower"])

    fig.update_layout(
        title=cfg.title,
        xaxis_title=cfg.x_label,
        yaxis_title=cfg.y_label,
        hovermode="closest",
    )

    return fig


_cached_figure: go.Figure | None = None


def get_cached_poincare_figure(config: PoincareConfig | None = None) -> go.Figure:
    """
    Retourne une figure Poincaré mise en cache.
    - Première invocation: construit et stocke la figure.
    - Si un config non None est passé: reconstruit avec cette config et met à jour le cache.
    - Appels suivants sans config: réutilisent la figure existante.
    """
    global _cached_figure
    if _cached_figure is None or config is not None:
        _cached_figure = build_poincare_figure(config)
    return _cached_figure


__all__ = ["PoincareConfig", "build_poincare_figure", "get_cached_poincare_figure"]

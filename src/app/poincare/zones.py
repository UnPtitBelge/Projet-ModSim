"""
Zones helpers for the Poincaré diagram.

Provides:
- generate_axes(): tau sampling axis
- generate_parabola(tau_vals): parabola values (delta = tau^2 / 4)
- generate_polygons(tau_vals, parabola_vals): zone polygon coordinates

Public API: generate_axes, generate_parabola, generate_polygons
"""

from __future__ import annotations

import numpy as np

from .constants import DELTA_MAX, N_SAMPLES, TAU_MAX, TAU_MIN


def generate_axes() -> np.ndarray:
    """
    Generate the 1D tau sampling axis.

    Returns:
        tau_vals: np.ndarray of shape (N_SAMPLES,)
    """
    return np.linspace(TAU_MIN, TAU_MAX, N_SAMPLES)


def generate_parabola(tau_vals: np.ndarray) -> np.ndarray:
    """
    Compute parabola values delta = tau^2 / 4 for given tau samples.

    Args:
        tau_vals: 1D array of tau samples

    Returns:
        delta_vals: 1D array of same shape as tau_vals
    """
    return (tau_vals**2) / 4.0


def generate_polygons(
    tau_vals: np.ndarray, parabola_vals: np.ndarray
) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    """
    Build polygon coordinate arrays for each zone.

    Zones logic (matching the original classification):
        Upper Left Zone:    tau < 0 and delta > parabola
        Upper Right Zone:   tau > 0 and delta > parabola
        Lower Left Zone:    tau < 0 and 0 < delta < parabola
        Lower Right Zone:   tau > 0 and 0 < delta < parabola
        Lower Zone:         delta < 0  (all tau)

    For filled polygons we construct (x, y) as:
        forward edge along parabola or baseline + backward edge along top/bottom limit.

    Args:
        tau_vals: 1D tau sampling array
        parabola_vals: 1D delta values of parabola

    Returns:
        dict mapping zone keys -> (x_array, y_array)
            Keys: "upper_left", "upper_right", "lower_left", "lower_right", "lower"
    """
    left_mask = tau_vals < 0
    right_mask = tau_vals > 0

    parabola_left = parabola_vals[left_mask]
    parabola_right = parabola_vals[right_mask]

    # Upper left: between parabola and DELTA_MAX for tau < 0
    UL_x = np.concatenate([tau_vals[left_mask], tau_vals[left_mask][::-1]])
    UL_y = np.concatenate([parabola_left, [DELTA_MAX] * len(parabola_left)])

    # Upper right: between parabola and DELTA_MAX for tau > 0
    UR_x = np.concatenate([tau_vals[right_mask], tau_vals[right_mask][::-1]])
    UR_y = np.concatenate([parabola_right, [DELTA_MAX] * len(parabola_right)])

    # Lower left: between parabola and 0 for tau < 0
    LL_x = np.concatenate([tau_vals[left_mask], tau_vals[left_mask][::-1]])
    LL_y = np.concatenate([parabola_left, [0] * len(parabola_left)])

    # Lower right: between parabola and 0 for tau > 0
    LR_x = np.concatenate([tau_vals[right_mask], tau_vals[right_mask][::-1]])
    LR_y = np.concatenate([parabola_right, [0] * len(parabola_right)])

    # Lower zone: between 0 and -DELTA_MAX for all tau
    LOW_x = np.concatenate([tau_vals, tau_vals[::-1]])
    LOW_y = np.concatenate([[0] * len(tau_vals), [-DELTA_MAX] * len(tau_vals)])

    return {
        "upper_left": (UL_x, UL_y),
        "upper_right": (UR_x, UR_y),
        "lower_left": (LL_x, LL_y),
        "lower_right": (LR_x, LR_y),
        "lower": (LOW_x, LOW_y),
    }


__all__ = ["generate_axes", "generate_parabola", "generate_polygons"]

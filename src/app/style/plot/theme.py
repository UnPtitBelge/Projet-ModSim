"""
Plot theming module for the Projet-ModSim web application.

This module provides a centralized Plotly figure theme and helper functions
to apply consistent styling (colors, line widths, fonts) across all figures.

Dependencies:
- src.app.style.palette (PALETTE)
- src.app.style.typography (TYPOGRAPHY)

Usage:
    from src.app.style.plot.theme import FIGURE_THEME, apply_to_figure, apply_zone_fill

    fig = make_figure_somewhere()
    apply_to_figure(fig)        # base layout, font, line/marker defaults
    # Optionally adjust zones by meta:
    for tr in fig.data:
        apply_zone_fill(tr)     # sets fillcolor for zones (ulp/urp/llp/lrp/lxa)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from src.app.style.palette import PALETTE
from src.app.style.typography import TYPOGRAPHY


@dataclass(frozen=True)
class FigureTheme:
    """Theme values for Plotly figures (colors, widths, sizes, backgrounds)."""

    # Lines and markers (defaults applied to accent traces)
    line_width: int = 6
    line_color: str = PALETTE.primary
    line_color_hover: str = PALETTE.primary_light  # Subtle change on hover
    marker_size: int = 6
    marker_color: str = PALETTE.primary

    # Zone fills (reference PALETTE for consistency - darker for better contrast)
    zone_upper_left: str = PALETTE.zone_upper_left
    zone_upper_right: str = PALETTE.zone_upper_right
    zone_lower_left: str = PALETTE.zone_lower_left
    zone_lower_right: str = PALETTE.zone_lower_right
    zone_lower_axis: str = PALETTE.zone_lower_axis

    # Zone hover states (subtle increase in opacity)
    zone_upper_left_hover: str = PALETTE.zone_upper_left_hover
    zone_upper_right_hover: str = PALETTE.zone_upper_right_hover
    zone_lower_left_hover: str = PALETTE.zone_lower_left_hover
    zone_lower_right_hover: str = PALETTE.zone_lower_right_hover
    zone_lower_axis_hover: str = PALETTE.zone_lower_axis_hover

    # Backgrounds
    plot_bgcolor: str = PALETTE.plot_bg
    paper_bgcolor: str = PALETTE.surface

    # Base font
    font_family: str = TYPOGRAPHY.font_sans
    font_size: int = 14  # base px
    font_color: str = PALETTE.text


# Singleton instance for import convenience
FIGURE_THEME = FigureTheme()


def _coerce_marker_size(size_val: Any, fallback: int) -> int:
    """Return a safe integer marker size given an arbitrary trace marker.size."""
    if isinstance(size_val, (int, float)):
        return max(int(size_val), int(fallback))
    # size may be None or other types; fallback safely
    return int(fallback)


def apply_to_figure(fig: Any, theme: Optional[FigureTheme] = None) -> None:
    """
    Apply base theming to a Plotly Figure instance:
    - Layout backgrounds and font
    - Accent lines/markers for common meta (parabola, axes)
    - Hide polygon borders for zone fills
    - Subtle hover effects on lines and zones
    """
    t = theme or FIGURE_THEME

    # Layout
    fig.update_layout(
        plot_bgcolor=t.plot_bgcolor,
        paper_bgcolor=t.paper_bgcolor,
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode="closest",
        font=dict(
            family=t.font_family,
            size=int(t.font_size * TYPOGRAPHY.size_md),
            color=t.font_color,
        ),
    )

    # Trace-level adjustments
    for tr in getattr(fig, "data", []):
        meta = getattr(tr, "meta", None)

        # Accent lines and markers for known meta keys (parabola and axes)
        if meta in {"parabola_left", "parabola_right", "y", "x_left", "x_right"}:
            # lines
            if hasattr(tr, "line") and tr.line is not None:
                tr.line.width = t.line_width
                if hasattr(tr.line, "color"):
                    tr.line.color = t.line_color
            # markers
            if hasattr(tr, "marker") and tr.marker is not None:
                size_val = getattr(tr.marker, "size", t.marker_size)
                tr.marker.size = _coerce_marker_size(size_val, t.marker_size)
                tr.marker.color = t.marker_color

        # Zones: set fillcolor and hide borders
        if meta in {"ulp", "urp", "llp", "lrp", "lxa"}:
            apply_zone_fill(tr, t)
            if hasattr(tr, "line") and tr.line is not None:
                # Hide polygon borders to keep fills clean
                tr.line.color = "rgba(0,0,0,0)"


def apply_zone_fill(trace: Any, theme: Optional[FigureTheme] = None) -> None:
    """
    Apply zone fill color to a trace based on its meta value.
    Expected meta: 'ulp', 'urp', 'llp', 'lrp', 'lxa'.
    """
    t = theme or FIGURE_THEME
    meta = getattr(trace, "meta", None)

    if not hasattr(trace, "fillcolor"):
        return

    if meta == "ulp":
        trace.fillcolor = t.zone_upper_left
    elif meta == "urp":
        trace.fillcolor = t.zone_upper_right
    elif meta == "llp":
        trace.fillcolor = t.zone_lower_left
    elif meta == "lrp":
        trace.fillcolor = t.zone_lower_right
    elif meta == "lxa":
        trace.fillcolor = t.zone_lower_axis


__all__ = ["FigureTheme", "FIGURE_THEME", "apply_to_figure", "apply_zone_fill"]

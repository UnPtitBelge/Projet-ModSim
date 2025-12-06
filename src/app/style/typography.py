"""
Typography module for the Projet-ModSim web application.

This module centralizes font families, size scale, line-heights, and font weights.
Other style modules (e.g., text styles, components) should import `TYPOGRAPHY`
from here to maintain consistency across the app.

Conventions:
- Sizes are expressed in rem units (use alongside f-strings when building styles).
- Line-heights are unitless multipliers.
- Weights follow common numeric values (400=regular, 500=medium, 600=semibold, 700=bold).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Typography:
    # Font families
    font_sans: str = (
        "Inter, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, "
        "'Fira Sans', 'Droid Sans', 'Helvetica Neue', Arial, 'Noto Sans', sans-serif"
    )
    font_mono: str = (
        "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "
        "'Liberation Mono', 'Courier New', monospace"
    )

    # Size scale (rem)
    size_base: float = 1.0
    size_sm: float = 0.925
    size_md: float = 1.0
    size_lg: float = 1.125
    size_xl: float = 1.375
    size_2xl: float = 1.75
    size_3xl: float = 2.25

    # Line-heights (unitless)
    lh_tight: float = 1.2
    lh_snug: float = 1.35
    lh_normal: float = 1.5

    # Font weights
    weight_regular: int = 400
    weight_medium: int = 500
    weight_semibold: int = 600
    weight_bold: int = 700


# Singleton instance for global import
TYPOGRAPHY = Typography()


def get_typography() -> Typography:
    """Return the global typography singleton."""
    return TYPOGRAPHY

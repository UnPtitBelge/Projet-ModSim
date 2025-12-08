"""
Palette module (soft modern) for the Projet-ModSim web application.

This module defines a centralized color palette to be used across the UI and plots.
It is intentionally small and dependency-free. Other style modules (typography, text,
components, plot theming) should import PALETTE from here to ensure consistency.

Conventions:
- Hex for solid colors
- RGBA strings for overlays/shadows
"""

from __future__ import annotations

"""
Color palette for the Projet-ModSim design system.

Implements a cohesive warm color scheme suitable for technical/mathematical
applications. All colors are defined in the PALETTE dataclass for easy
access and maintenance.

Color Categories:

1. Core Colors (UI background & text):
   - bg: #FEF5F1 (warm beige-peach background)
   - surface: #FFFBF8 (warm white, cards/sections)
   - primary: #EA580C (warm orange, accents/buttons)
   - text: #3E2723 (dark brown, main text)

2. Accessibility:
   - border: #E8DDD4 (warm beige borders)
   - muted: #9E8B7E (muted brown for secondary text)
   - overlay: rgba(62, 39, 35, 0.06) (brown at 6% opacity)
   - shadow: rgba(62, 39, 35, 0.08) (brown at 8% opacity)

3. Poincaré Diagram Zones (stability regions):
   - Upper left/right/lower regions with base, hover, and active states
   - Warm oranges for highlighting
   - Cool grays for axis regions

4. Special:
   - mouvement_uniforme: #F59E0B (amber accent)
   - white, black: Standard values for overlays/text

The palette is frozen (immutable) to prevent accidental modifications.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Palette:
    # Brand / primary (warm tones)
    primary: str = "#EA580C"  # Warm Orange
    primary_light: str = "#F97316"  # Orange 500
    primary_dark: str = "#D63803"  # Darker Orange

    # Secondary / success
    secondary: str = "#DC2626"  # Warm Red

    # Accents
    accent_amber: str = "#F59E0B"  # Amber 500
    accent_red: str = "#EF4444"  # Red 500

    # Greys
    bg: str = "#FEF5F1"  # Warm off-white (slightly peachy)
    surface: str = "#FFFBF8"  # Warm white (slightly warm)
    text: str = "#3E2723"  # Dark brown (warmer than slate)
    text_muted: str = "#78614B"  # Warm brown-grey
    border: str = "#E8DDD4"  # Warm beige (warmer than slate)

    # Utility (RGBA)
    overlay: str = "rgba(62, 39, 35, 0.06)"  # Dark brown @ 6% (hover bg)
    shadow: str = "rgba(62, 39, 35, 0.08)"  # Dark brown @ 8% (box shadow)

    # Poincaré diagram zones (warm color scheme - refined)
    zone_upper_left: str = "rgba(245, 158, 11, 0.35)"  # Warm Amber @ 35%
    zone_upper_right: str = "rgba(239, 68, 68, 0.35)"  # Warm Red @ 35%
    zone_lower_left: str = "rgba(74, 222, 128, 0.38)"  # Bright Green @ 38%
    zone_lower_right: str = "rgba(251, 146, 60, 0.32)"  # Orange @ 32%
    zone_lower_axis: str = "rgba(209, 213, 219, 0.45)"  # Cool Gray @ 45%

    # Poincaré diagram background (clean and neutral)
    plot_bg: str = "#FAFAF8"  # Warm neutral off-white

    # Poincaré diagram hover zones (subtle increase)
    zone_upper_left_hover: str = "rgba(245, 158, 11, 0.50)"  # Warm Amber @ 50%
    zone_upper_right_hover: str = "rgba(239, 68, 68, 0.50)"  # Warm Red @ 50%
    zone_lower_left_hover: str = "rgba(74, 222, 128, 0.53)"  # Bright Green @ 53%
    zone_lower_right_hover: str = "rgba(251, 146, 60, 0.47)"  # Orange @ 47%
    zone_lower_axis_hover: str = "rgba(209, 213, 219, 0.60)"  # Cool Gray @ 60%

    # Mouvement uniforme point color
    mouvement_uniforme: str = "#F59E0B"  # Amber 500 (warm accent)


# Singleton palette instance
PALETTE = Palette()


def get_palette() -> Palette:
    """Return the global palette singleton."""
    return PALETTE

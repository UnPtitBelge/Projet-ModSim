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
    # Brand / primary (terra cotta tones)
    primary: str = "#C65D3B"  # Terra Cotta
    primary_light: str = "#D97855"  # Light Terra Cotta
    primary_dark: str = "#A34A28"  # Dark Terra Cotta

    # Secondary / complementary
    secondary: str = "#3B7C8C"  # Teal Blue (complementary to terra cotta)
    secondary_light: str = "#6FA8DC"  # Light Teal Blue
    secondary_dark: str = "#25496B"  # Dark Teal Blue

    # Third / accent
    third: str = "#F2B134"  # Golden Yellow
    third_light: str = "#FFD580"  # Light Golden Yellow
    third_dark: str = "#B97A1B"  # Dark Golden Yellow

    # Accents
    accent_amber: str = "#E8A870"  # Warm Sand/Amber
    accent_red: str = "#B85A45"  # Burnt Sienna

    # Greys (warmer, earthier tones)
    bg: str = "#F9F3EE"  # Warm cream background
    surface: str = "#FFF9F5"  # Very light warm white
    text: str = "#3D2E27"  # Deep warm brown
    text_muted: str = "#8B7366"  # Muted warm brown
    border: str = "#E5D5C8"  # Warm beige border

    # Utility (RGBA)
    overlay: str = "rgba(61, 46, 39, 0.06)"  # Deep brown @ 6% (hover bg)
    shadow: str = "rgba(61, 46, 39, 0.08)"  # Deep brown @ 8% (box shadow)

    # Poincaré diagram zones (terra cotta harmony)
    zone_upper_left: str = "rgba(232, 168, 112, 0.35)"  # Warm Sand @ 35%
    zone_upper_right: str = "rgba(184, 90, 69, 0.35)"  # Burnt Sienna @ 35%
    zone_lower_left: str = "rgba(88, 150, 137, 0.38)"  # Sage Green @ 38%
    zone_lower_right: str = "rgba(217, 120, 85, 0.32)"  # Light Terra @ 32%
    zone_lower_axis: str = "rgba(200, 190, 180, 0.45)"  # Warm Gray @ 45%

    # Poincaré diagram background (clean and neutral)
    plot_bg: str = "#FDFAF7"  # Very light warm neutral

    # Poincaré diagram hover zones (subtle increase)
    zone_upper_left_hover: str = "rgba(232, 168, 112, 0.50)"  # Warm Sand @ 50%
    zone_upper_right_hover: str = "rgba(184, 90, 69, 0.50)"  # Burnt Sienna @ 50%
    zone_lower_left_hover: str = "rgba(88, 150, 137, 0.53)"  # Sage Green @ 53%
    zone_lower_right_hover: str = "rgba(217, 120, 85, 0.47)"  # Light Terra @ 47%
    zone_lower_axis_hover: str = "rgba(200, 190, 180, 0.60)"  # Warm Gray @ 60%

    # Mouvement uniforme point color
    mouvement_uniforme: str = "#E8A870"  # Warm Sand (harmonious accent)

    # Stability category colors (terra cotta harmony)
    stability_stable: str = "#589689"  # Sage Green (earthy, stable)
    stability_marginal: str = "#D9925D"  # Warm Terracotta Orange (transitional)
    stability_unstable: str = "#B85A45"  # Burnt Sienna (unstable, warm red)


# Singleton palette instance
PALETTE = Palette()


def get_palette() -> Palette:
    """Return the global palette singleton."""
    return PALETTE

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

from dataclasses import dataclass


@dataclass(frozen=True)
class Palette:
    # Brand / primary
    primary: str = "#4F46E5"  # Indigo 600
    primary_light: str = "#6366F1"  # Indigo 500
    primary_dark: str = "#4338CA"  # Indigo 700

    # Secondary / success
    secondary: str = "#10B981"  # Emerald 500

    # Accents
    accent_amber: str = "#F59E0B"  # Amber 500
    accent_red: str = "#EF4444"  # Red 500

    # Greys
    bg: str = "#F8FAFC"  # Gray 50 (main app background)
    surface: str = "#FFFFFF"  # White (cards, panels)
    text: str = "#0F172A"  # Slate 900 (primary text)
    text_muted: str = "#475569"  # Slate 600 (secondary text)
    border: str = "#E2E8F0"  # Slate 200 (borders, separators)

    # Utility (RGBA)
    overlay: str = "rgba(15, 23, 42, 0.06)"  # Slate 900 @ 6% (hover bg)
    shadow: str = "rgba(15, 23, 42, 0.08)"  # Slate 900 @ 8% (box shadow)


# Singleton palette instance
PALETTE = Palette()


def get_palette() -> Palette:
    """Return the global palette singleton."""
    return PALETTE

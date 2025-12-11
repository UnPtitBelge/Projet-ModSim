"""
Sidebar component styles for the Projet-ModSim web application.

This module centralizes style dictionaries and small helpers for the left
navigation sidebar: container, headers, links, and sub-sections. It builds
on the shared palette and typography modules to ensure consistent visuals
across the app.

Usage (example within Dash layouts):
    from src.app.style.components.sidebar import (
        SIDEBAR_WIDTH,
        sidebar_container,
        sidebar_header,
        nav_link,
        nav_subtitle,
    )

    html.Div(
        [
            html.H3("Menu", style=sidebar_header()),
            html.A("Accueil", href="/", style=nav_link()),
            html.A("Poincaré", href="/poincare", style=nav_link(active=True)),
            html.H4("Stabilité", style=nav_subtitle()),
            html.A("Foyer stable", href="/stabilite/foyer_stable", style=nav_link(level=1)),
        ],
        style=sidebar_container(),
    )

Notes:
- Inline styles are returned as dict[str, str] suitable for Dash components.
- Hover states are suggested via `nav_link_hover_guide()` and can be applied
  using className and external CSS if needed.
"""

from __future__ import annotations

from typing import Dict

from src.app.style.palette import PALETTE
from src.app.style.text import TEXT
from src.app.style.typography import TYPOGRAPHY

# Public constants
SIDEBAR_WIDTH: int = 200


def sidebar_container() -> Dict[str, str]:
    """Left sidebar container: fixed, scrollable, card-like surface."""
    return {
        "position": "fixed",
        "top": "0",
        "left": "0",
        "bottom": "0",
        "width": f"{SIDEBAR_WIDTH}px",
        "overflowY": "auto",
        "padding": "18px 16px",
        "backgroundColor": PALETTE.surface,
        "borderRight": f"1px solid {PALETTE.border}",
        "boxShadow": f"0 2px 12px 0 {PALETTE.shadow}",
    }


def sidebar_header() -> Dict[str, str]:
    """Primary header for the sidebar (e.g., 'Menu')."""
    style = dict(TEXT["h3"])
    style.update(
        {
            "margin": "0 0 16px 0",
            "color": PALETTE.primary,
        }
    )
    return style


def nav_subtitle() -> Dict[str, str]:
    """Secondary header inside the sidebar (group label)."""
    return {
        "fontFamily": TYPOGRAPHY.font_sans,
        "fontSize": f"{TYPOGRAPHY.size_md}rem",
        "lineHeight": f"{TYPOGRAPHY.lh_snug}",
        "color": PALETTE.text_muted,
        "fontWeight": str(TYPOGRAPHY.weight_semibold),
        "margin": "16px 0 8px 6px",
        "letterSpacing": "-0.01em",
    }


def nav_link(active: bool = False, level: int = 0) -> Dict[str, str]:
    """
    Navigation link style with optional active state and indentation level.
    `level` controls left margin to visually indicate sub-pages (0..2).
    """
    indent_px = 6 + max(0, min(level, 3)) * 10
    base = {
        "display": "block",
        "padding": "10px 12px",
        "margin": f"2px 0 2px {indent_px}px",
        "color": PALETTE.text,
        "textDecoration": "none",
        "borderRadius": "8px",
        "transition": "background-color 120ms ease, color 120ms ease",
        "fontFamily": TYPOGRAPHY.font_sans,
        "fontSize": f"{TYPOGRAPHY.size_md}rem",
        "lineHeight": f"{TYPOGRAPHY.lh_snug}",
        "fontWeight": str(TYPOGRAPHY.weight_regular),
    }
    if active:
        base.update(
            {
                "backgroundColor": PALETTE.overlay,
                "color": PALETTE.primary_dark,
                "fontWeight": str(TYPOGRAPHY.weight_medium),
            }
        )
    return base


def nav_link_hover_guide() -> Dict[str, str]:
    """
    Suggested hover colors for nav links. Use this as a reference to implement
    hover styles via className and external CSS if desired.
    """
    return {
        "backgroundColor": PALETTE.overlay,
        "color": PALETTE.primary_dark,
    }


def divider() -> Dict[str, str]:
    """Thin horizontal divider for grouping items."""
    return {
        "height": "1px",
        "backgroundColor": PALETTE.border,
        "border": "none",
        "margin": "12px 6px",
    }


def footer_text() -> Dict[str, str]:
    """Muted small text style suitable for a footer note in the sidebar."""
    style = dict(TEXT["small"])
    style.update(
        {
            "margin": "14px 6px 0 6px",
        }
    )
    return style


def chaos_badge() -> Dict[str, str]:
    """Unique badge style for chaos page in sidebar: orange rounded rectangle."""
    return {
        "display": "block",
        "padding": "12px 14px",
        "margin": "12px 6px",
        "backgroundColor": PALETTE.primary,
        "color": PALETTE.surface,
        "borderRadius": "12px",
        "textAlign": "center",
        "textDecoration": "none",
        "fontFamily": TYPOGRAPHY.font_sans,
        "fontSize": f"{TYPOGRAPHY.size_md}rem",
        "fontWeight": str(TYPOGRAPHY.weight_semibold),
        "transition": "all 120ms ease",
        "boxShadow": f"0 2px 8px 0 rgba(234, 88, 12, 0.2)",
    }


def chaos_badge_hover() -> Dict[str, str]:
    """Hover state for chaos badge."""
    return {
        "display": "block",
        "padding": "12px 14px",
        "margin": "12px 6px",
        "backgroundColor": PALETTE.primary_dark,
        "color": PALETTE.surface,
        "borderRadius": "12px",
        "textAlign": "center",
        "textDecoration": "none",
        "fontFamily": TYPOGRAPHY.font_sans,
        "fontSize": f"{TYPOGRAPHY.size_md}rem",
        "fontWeight": str(TYPOGRAPHY.weight_semibold),
        "transition": "all 120ms ease",
        "boxShadow": f"0 4px 12px 0 rgba(234, 88, 12, 0.35)",
    }


__all__ = [
    "SIDEBAR_WIDTH",
    "sidebar_container",
    "sidebar_header",
    "nav_subtitle",
    "nav_link",
    "nav_link_hover_guide",
    "divider",
    "footer_text",
    "chaos_badge",
    "chaos_badge_hover",
]

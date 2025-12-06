"""
Layout components and container styles for the Projet-ModSim web application.

This module centralizes common layout style dictionaries used across pages:
- Application container (page background and base typography)
- Content wrapper (main area offset by the sidebar)
- Page text container (max width and text flow)
- Graph container (card-like wrapper around figures)
- Section card (generic content card)

All styles are inline (dict[str, str]) for use in Dash components.

Usage:
    from src.app.style.components.layout import (
        app_container,
        content_wrapper,
        page_text_container,
        graph_container,
        section_card,
    )

    html.Div([...], style=app_container())
    html.Div([...], style=content_wrapper())
    html.Div([...], style=page_text_container(920))
    html.Div([dcc.Graph(...)], style=graph_container())
"""

from __future__ import annotations

from typing import Dict

from src.app.style.components.sidebar import SIDEBAR_WIDTH
from src.app.style.palette import PALETTE
from src.app.style.typography import TYPOGRAPHY


def app_container() -> Dict[str, str]:
    """Main app container: background and base text settings."""
    return {
        "backgroundColor": PALETTE.bg,
        "minHeight": "100vh",
        "color": PALETTE.text,
        "fontFamily": TYPOGRAPHY.font_sans,
    }


def content_wrapper(padding_px: int = 24) -> Dict[str, str]:
    """
    Wrapper for main content area (right of the fixed sidebar).
    The margin-left equals the sidebar width to prevent overlap.
    """
    return {
        "marginLeft": f"{SIDEBAR_WIDTH}px",
        "padding": f"{padding_px}px",
    }


def page_text_container(max_width_px: int = 920) -> Dict[str, str]:
    """Constrain text content to a readable width and harmonize typography."""
    return {
        "maxWidth": f"{max_width_px}px",
        "padding": "0",
        "lineHeight": f"{TYPOGRAPHY.lh_normal}",
        "fontSize": f"{TYPOGRAPHY.size_md}rem",
        "color": PALETTE.text,
    }


def graph_container(padding_px: int = 8) -> Dict[str, str]:
    """Card-like container for figures and graphs."""
    return {
        "backgroundColor": PALETTE.surface,
        "border": f"1px solid {PALETTE.border}",
        "borderRadius": "12px",
        "padding": f"{padding_px}px",
        "boxShadow": f"0 2px 8px 0 {PALETTE.shadow}",
    }


def section_card(padding_px: int = 18) -> Dict[str, str]:
    """Generic section card for grouped content blocks."""
    return {
        "backgroundColor": PALETTE.surface,
        "border": f"1px solid {PALETTE.border}",
        "borderRadius": "12px",
        "padding": f"{padding_px}px",
        "boxShadow": f"0 2px 8px 0 {PALETTE.shadow}",
    }


__all__ = [
    "app_container",
    "content_wrapper",
    "page_text_container",
    "graph_container",
    "section_card",
]

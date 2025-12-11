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


def content_wrapper(
    padding_px: int = 24, margin_left_px: int = SIDEBAR_WIDTH // 2
) -> Dict[str, str]:
    """
    Wrapper for main content area (right of the fixed sidebar).
    The margin-left equals the sidebar width to prevent overlap.
    """
    return {
        "marginLeft": f"{margin_left_px}px",
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


def side_by_side_container(
    width_percent: int = 48, margin_right_percent: int = 4
) -> Dict[str, str]:
    """Container for placing elements side-by-side (e.g., two graphs or two cards)."""
    return {
        "width": f"{width_percent}%",
        "display": "inline-block",
        "marginRight": f"{margin_right_percent}%",
        "verticalAlign": "top",
    }


def side_by_side_last(width_percent: int = 48) -> Dict[str, str]:
    """Last element in side-by-side layout (no right margin)."""
    return {
        "width": f"{width_percent}%",
        "display": "inline-block",
        "verticalAlign": "top",
    }


def code_display(padding_px: int = 12) -> Dict[str, str]:
    """Container for code or preformatted text display."""
    return {
        "padding": f"{padding_px}px",
        "backgroundColor": PALETTE.bg,
        "borderRadius": "8px",
        "border": f"1px solid {PALETTE.border}",
        "fontFamily": "monospace",
        "fontSize": "0.9rem",
    }


def nav_button(
    kind: str = "primary", padding_px: int = 12, padding_horizontal: int = 24
) -> Dict[str, str]:
    """
    Navigation button style (for html.A links styled as buttons).

    Args:
        kind: "primary" (filled) or "secondary" (outlined)
        padding_px: vertical padding
        padding_horizontal: horizontal padding
    """
    if kind == "primary":
        return {
            "display": "inline-block",
            "padding": f"{padding_px}px {padding_horizontal}px",
            "backgroundColor": PALETTE.primary,
            "color": PALETTE.surface,
            "textDecoration": "none",
            "borderRadius": "8px",
            "fontWeight": "600",
            "marginRight": "12px",
        }
    else:  # secondary
        return {
            "display": "inline-block",
            "padding": f"{padding_px}px {padding_horizontal}px",
            "backgroundColor": PALETTE.surface,
            "color": PALETTE.primary,
            "textDecoration": "none",
            "borderRadius": "8px",
            "fontWeight": "600",
            "border": f"2px solid {PALETTE.primary}",
            "marginRight": "12px",
        }


def spacing_section(spacing_type: str = "top") -> Dict[str, str]:
    """
    Standardized spacing for sections.

    Args:
        spacing_type: "top", "bottom", "both", "small"
    """
    spacing_map = {
        "top": {"marginTop": "24px"},
        "bottom": {"marginBottom": "24px"},
        "both": {"marginTop": "24px", "marginBottom": "24px"},
        "small": {"marginTop": "16px"},
    }
    return spacing_map.get(spacing_type, {})


def back_link() -> Dict[str, str]:
    """Back/return link style."""
    return {
        "marginBottom": "16px",
        "padding": "8px 12px",
        "backgroundColor": PALETTE.bg,
        "color": PALETTE.primary,
        "textDecoration": "none",
        "borderRadius": "8px",
        "fontSize": f"{TYPOGRAPHY.size_sm}rem",
        "fontWeight": str(TYPOGRAPHY.weight_semibold),
        "border": f"1px solid {PALETTE.border}",
        "transition": "all 0.2s ease",
        "display": "inline-block",
    }


def action_button() -> Dict[str, str]:
    """Action button style (for html.Button elements)."""
    return {
        "padding": "10px 20px",
        "margin": "10px 0",
        "backgroundColor": PALETTE.primary,
        "color": PALETTE.surface,
        "border": "none",
        "borderRadius": "8px",
        "cursor": "pointer",
        "fontSize": "14px",
        "fontWeight": "600",
        "transition": "all 0.2s ease",
    }


def loading_container(padding_px: int = 12) -> Dict[str, str]:
    """
    Container style for dcc.Loading spinner.

    Provides a consistent appearance with soft colors and spacing.
    """
    return {
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "center",
        "minHeight": "300px",
        "color": PALETTE.primary,
        "fontFamily": TYPOGRAPHY.font_sans,
    }


def alert_box(kind: str = "info") -> Dict[str, str]:
    """
    Alert/notice box style for informational messages, warnings, or tips.

    Args:
        kind: "info" (default), "warning", or "tip"

    Returns:
        Style dictionary for the alert box
    """
    base = {
        "padding": "10px 12px",
        "borderRadius": "4px",
        "fontSize": f"{TYPOGRAPHY.size_sm}rem",
        "fontFamily": TYPOGRAPHY.font_sans,
        "lineHeight": f"{TYPOGRAPHY.lh_normal}",
        "margin": "8px 0",
    }

    if kind == "warning":
        return {
            **base,
            "backgroundColor": "#f5f5f5",
            "color": PALETTE.text_muted,
            "borderLeft": f"3px solid {PALETTE.text_muted}",
        }
    elif kind == "tip":
        return {
            **base,
            "backgroundColor": "#FFF9F0",
            "color": PALETTE.text,
            "borderLeft": f"3px solid {PALETTE.primary}",
        }
    else:  # info
        return {
            **base,
            "backgroundColor": PALETTE.bg,
            "color": PALETTE.text_muted,
            "borderLeft": f"3px solid {PALETTE.border}",
        }


__all__ = [
    "app_container",
    "content_wrapper",
    "page_text_container",
    "graph_container",
    "section_card",
    "side_by_side_container",
    "side_by_side_last",
    "code_display",
    "nav_button",
    "spacing_section",
    "back_link",
    "action_button",
    "loading_container",
    "alert_box",
]

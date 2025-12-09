"""
Tooltip styling for the Projet-ModSim application.

Provides consistent tooltip styles using the project's color palette.
"""

from ..palette import PALETTE


# Tooltip style for dbc.Tooltip components
TOOLTIP_STYLE = {
    "backgroundColor": f"{PALETTE.surface} !important",
    "color": f"{PALETTE.text} !important",
    "border": f"1px solid {PALETTE.border} !important",
    "fontSize": "13px",
    "padding": "8px 10px",
}


def get_tooltip_style() -> dict[str, str]:
    """
    Return the standard tooltip style dictionary.
    
    Returns:
        Dictionary of CSS properties for tooltip styling.
    """
    return TOOLTIP_STYLE.copy()

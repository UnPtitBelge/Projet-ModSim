"""
Text styles module for the Projet-ModSim web application.

Provides ready-to-use style dictionaries for headings, paragraphs, muted text,
small text, and code blocks. Centralizes typography and color usage to keep
the UI consistent. Designed for inline styles in Dash components.

Usage:
    from src.app.style.text import TEXT, get_text_styles
    html.H1("Titre", style=TEXT["h1"])
    html.P("Paragraphe", style=TEXT["p"])
"""

from __future__ import annotations

from .palette import PALETTE
from .typography import TYPOGRAPHY

# Headings
H1 = {
    "fontFamily": TYPOGRAPHY.font_sans,
    "fontSize": f"{TYPOGRAPHY.size_3xl}rem",
    "lineHeight": f"{TYPOGRAPHY.lh_tight}",
    "color": PALETTE.text,
    "fontWeight": str(TYPOGRAPHY.weight_bold),
    "margin": "0 0 16px 0",
    "letterSpacing": "-0.02em",
}

H2 = {
    "fontFamily": TYPOGRAPHY.font_sans,
    "fontSize": f"{TYPOGRAPHY.size_2xl}rem",
    "lineHeight": f"{TYPOGRAPHY.lh_tight}",
    "color": PALETTE.text,
    "fontWeight": str(TYPOGRAPHY.weight_semibold),
    "margin": "24px 0 12px 0",
    "letterSpacing": "-0.01em",
}

H3 = {
    "fontFamily": TYPOGRAPHY.font_sans,
    "fontSize": f"{TYPOGRAPHY.size_xl}rem",
    "lineHeight": f"{TYPOGRAPHY.lh_snug}",
    "color": PALETTE.text,
    "fontWeight": str(TYPOGRAPHY.weight_semibold),
    "margin": "20px 0 10px 0",
}

# Paragraph and small text
P = {
    "fontFamily": TYPOGRAPHY.font_sans,
    "fontSize": f"{TYPOGRAPHY.size_md}rem",
    "lineHeight": f"{TYPOGRAPHY.lh_normal}",
    "color": PALETTE.text,
    "fontWeight": str(TYPOGRAPHY.weight_regular),
    "margin": "0 0 12px 0",
}

MUTED = {
    **P,
    "color": PALETTE.text_muted,
}

SMALL = {
    "fontFamily": TYPOGRAPHY.font_sans,
    "fontSize": f"{TYPOGRAPHY.size_sm}rem",
    "lineHeight": f"{TYPOGRAPHY.lh_snug}",
    "color": PALETTE.text_muted,
    "fontWeight": str(TYPOGRAPHY.weight_regular),
}

# Monospace code block
CODE_BLOCK = {
    "fontFamily": TYPOGRAPHY.font_mono,
    "fontSize": f"{TYPOGRAPHY.size_sm}rem",
    "background": PALETTE.bg,
    "border": f"1px solid {PALETTE.border}",
    "borderRadius": "8px",
    "padding": "10px 12px",
    "color": PALETTE.text,
    "whiteSpace": "pre-wrap",
}

# Export dictionary for convenience
TEXT = {
    "h1": H1,
    "h2": H2,
    "h3": H3,
    "p": P,
    "muted": MUTED,
    "small": SMALL,
    "code_block": CODE_BLOCK,
}


def get_text_styles():
    """Return a copy of the text styles dictionary for safe consumption."""
    return dict(TEXT)


__all__ = ["TEXT", "get_text_styles"]

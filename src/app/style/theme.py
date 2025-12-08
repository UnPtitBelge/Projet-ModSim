"""
Centralized theme module for the web application:
- Palette (modern, soft, accessible)
- Typography scale and weights
- Layout helpers and component style factories
- Plotly figure theming helpers

Usage (examples):
    from src.app.style.theme import PALETTE, TYPO, style_app_container, style_sidebar, text, figure_theme

    # In Dash layouts:
    html.Div([...], style=style_app_container())
    html.Div([...], style=style_sidebar())
    html.H1("Titre", style=text.h1)
    html.P("Paragraphe", style=text.p)

    # With Plotly:
    fig = build_poincare_figure()
    figure_theme.apply_to_figure(fig)

Note: All styles are plain dicts to avoid external dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

# Import the centralized palette
from src.app.style.palette import PALETTE as MAIN_PALETTE


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

    # Utility
    overlay: str = "rgba(62, 39, 35, 0.06)"  # Dark brown @ 6%
    shadow: str = "rgba(62, 39, 35, 0.08)"  # Dark brown @ 8%


PALETTE = Palette()


# ---- Typography scale --------------------------------------------------------


@dataclass(frozen=True)
class Typography:
    # Font families
    font_sans: str = (
        "Inter, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', Arial, 'Noto Sans', sans-serif"
    )
    font_mono: str = (
        "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace"
    )

    # Sizes (rem)
    size_base: float = 1.0
    size_sm: float = 0.925
    size_md: float = 1.0
    size_lg: float = 1.125
    size_xl: float = 1.375
    size_2xl: float = 1.75
    size_3xl: float = 2.25

    # Line-heights
    lh_tight: float = 1.2
    lh_snug: float = 1.35
    lh_normal: float = 1.5

    # Weights
    weight_regular: int = 400
    weight_medium: int = 500
    weight_semibold: int = 600
    weight_bold: int = 700


TYPO = Typography()


# ---- Text styles (ready-to-use dicts) ----------------------------------------


class text:
    # Titles
    h1 = {
        "fontFamily": TYPO.font_sans,
        "fontSize": f"{TYPO.size_3xl}rem",
        "lineHeight": TYPO.lh_tight,
        "color": PALETTE.text,
        "fontWeight": TYPO.weight_bold,
        "fontStyle": "normal",
        "margin": "0 0 16px 0",
        "letterSpacing": "-0.02em",
    }
    h2 = {
        "fontFamily": TYPO.font_sans,
        "fontSize": f"{TYPO.size_2xl}rem",
        "lineHeight": TYPO.lh_tight,
        "color": PALETTE.text,
        "fontWeight": TYPO.weight_semibold,
        "fontStyle": "normal",
        "margin": "24px 0 12px 0",
        "letterSpacing": "-0.01em",
    }
    h3 = {
        "fontFamily": TYPO.font_sans,
        "fontSize": f"{TYPO.size_xl}rem",
        "lineHeight": TYPO.lh_snug,
        "color": PALETTE.text,
        "fontWeight": TYPO.weight_semibold,
        "fontStyle": "normal",
        "margin": "20px 0 10px 0",
    }

    # Paragraph and small
    p = {
        "fontFamily": TYPO.font_sans,
        "fontSize": f"{TYPO.size_md}rem",
        "lineHeight": TYPO.lh_normal,
        "color": PALETTE.text,
        "fontWeight": TYPO.weight_regular,
        "fontStyle": "normal",
        "margin": "0 0 12px 0",
    }
    muted = {
        **p,
        "color": PALETTE.text_muted,
    }
    small = {
        "fontFamily": TYPO.font_sans,
        "fontSize": f"{TYPO.size_sm}rem",
        "lineHeight": TYPO.lh_snug,
        "color": PALETTE.text_muted,
        "fontWeight": TYPO.weight_regular,
        "fontStyle": "normal",
    }

    # Monospace block
    code_block = {
        "fontFamily": TYPO.font_mono,
        "fontSize": f"{TYPO.size_sm}rem",
        "background": PALETTE.bg,
        "border": f"1px solid {PALETTE.border}",
        "borderRadius": "8px",
        "padding": "10px 12px",
        "color": PALETTE.text,
        "whiteSpace": "pre-wrap",
    }


# ---- Component style helpers -------------------------------------------------


def style_app_container() -> Dict[str, str]:
    """Main app container (page background and base text)."""
    return {
        "backgroundColor": PALETTE.bg,
        "minHeight": "100vh",
        "color": PALETTE.text,
        "fontFamily": TYPO.font_sans,
    }


def style_content_wrapper() -> Dict[str, str]:
    """Wrapper for the main content area (right of sidebar)."""
    return {
        "marginLeft": "280px",
        "padding": "24px",
    }


def style_sidebar() -> Dict[str, str]:
    """Left sidebar: navigation, grouped links, subtle separators."""
    return {
        "position": "fixed",
        "top": "0",
        "left": "0",
        "bottom": "0",
        "width": "280px",
        "overflowY": "auto",
        "padding": "18px 16px",
        "backgroundColor": PALETTE.surface,
        "borderRight": f"1px solid {PALETTE.border}",
        "boxShadow": f"0 2px 12px 0 {PALETTE.shadow}",
    }


def style_sidebar_header() -> Dict[str, str]:
    return {
        **text.h3,
        "margin": "0 0 16px 0",
        "color": PALETTE.primary,
    }


def style_sidebar_link(active: bool = False) -> Dict[str, str]:
    base = {
        "display": "block",
        "padding": "10px 12px",
        "color": PALETTE.text,
        "textDecoration": "none",
        "borderRadius": "8px",
        "transition": "background-color 120ms ease, color 120ms ease",
        "margin": "2px 0",
    }
    if active:
        base.update(
            {
                "backgroundColor": PALETTE.overlay,
                "color": PALETTE.primary_dark,
                "fontWeight": str(TYPO.weight_medium),
            }
        )
    return base


def style_sidebar_link_hover() -> Dict[str, str]:
    """Hint: in Dash, you can apply hover via className + external CSS; here we provide a color guide."""
    return {
        "backgroundColor": PALETTE.overlay,
        "color": PALETTE.primary_dark,
    }


def style_section_card() -> Dict[str, str]:
    """Generic card for content sections."""
    return {
        "backgroundColor": PALETTE.surface,
        "border": f"1px solid {PALETTE.border}",
        "borderRadius": "12px",
        "padding": "18px",
        "boxShadow": f"0 2px 8px 0 {PALETTE.shadow}",
    }


def style_page_text_container(max_width_px: int = 920) -> Dict[str, str]:
    return {
        "maxWidth": f"{max_width_px}px",
        "padding": "0",
        "lineHeight": f"{TYPO.lh_normal}",
        "fontSize": f"{TYPO.size_md}rem",
        "color": PALETTE.text,
    }


def style_graph_container() -> Dict[str, str]:
    return {
        "backgroundColor": PALETTE.surface,
        "border": f"1px solid {PALETTE.border}",
        "borderRadius": "12px",
        "padding": "8px",
        "boxShadow": f"0 2px 8px 0 {PALETTE.shadow}",
    }


def style_button(kind: str = "primary") -> Dict[str, str]:
    """Simple button style (for html.A links styled as buttons)."""
    bg, fg = (
        (PALETTE.primary, "#FFFFFF")
        if kind == "primary"
        else (PALETTE.secondary, "#062b20")
    )
    return {
        "display": "inline-block",
        "padding": "10px 14px",
        "backgroundColor": bg,
        "color": fg,
        "textDecoration": "none",
        "borderRadius": "10px",
        "fontWeight": str(TYPO.weight_medium),
        "border": "none",
        "transition": "opacity 120ms ease",
    }


# ---- Plotly figure theming ---------------------------------------------------


@dataclass(frozen=True)
class FigureTheme:
    """Theme values for Plotly figures."""

    line_width: int = 6
    line_color: str = PALETTE.primary
    marker_size: int = 6
    marker_color: str = PALETTE.primary

    # Zone fills (aligned to palette, soft transparencies)
    zone_upper_left: str = "rgba(245, 158, 11, 0.28)"  # Amber 500 @ ~28%
    zone_upper_right: str = "rgba(99, 102, 241, 0.28)"  # Indigo 500 @ ~28%
    zone_lower_left: str = "rgba(16, 185, 129, 0.30)"  # Emerald 500 @ 30%
    zone_lower_right: str = "rgba(79, 70, 229, 0.20)"  # Indigo 600 @ 20%
    zone_lower_axis: str = "rgba(226, 232, 240, 0.45)"  # Slate 200 @ 45%

    # Background and axes
    plot_bgcolor: str = PALETTE.surface


figure_theme = FigureTheme()


def apply_to_figure(fig) -> None:
    """
    Apply base theming to a Plotly Figure instance (lines, markers, layout).
    Safe to call after traces are added; updates layout and accentuates known traces via meta.
    """
    # Update layout
    fig.update_layout(
        plot_bgcolor=figure_theme.plot_bgcolor,
        paper_bgcolor=PALETTE.surface,
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode="closest",
        font=dict(
            family=TYPO.font_sans,
            size=int(14 * TYPO.size_md),
            color=PALETTE.text,
        ),
    )

    # Update traces by meta (if any)
    for tr in getattr(fig, "data", []):
        meta = getattr(tr, "meta", None)
        # Accent lines and markers
        if meta in {"parabola_left", "parabola_right", "y", "x_left", "x_right"}:
            if hasattr(tr, "line") and tr.line:
                tr.line.width = figure_theme.line_width
                if hasattr(tr.line, "color"):
                    tr.line.color = figure_theme.line_color
            if hasattr(tr, "marker") and tr.marker:
                size_val = getattr(tr.marker, "size", figure_theme.marker_size)
                # Guard against None or non-numeric sizes
                if not isinstance(size_val, (int, float)) or size_val is None:
                    size_val = figure_theme.marker_size
                tr.marker.size = max(int(size_val), int(figure_theme.marker_size))
                tr.marker.color = figure_theme.marker_color
        # Zones fill
        if meta in {"ulp", "urp", "llp", "lrp", "lxa"}:
            if hasattr(tr, "fillcolor"):
                if meta == "ulp":
                    tr.fillcolor = figure_theme.zone_upper_left
                elif meta == "urp":
                    tr.fillcolor = figure_theme.zone_upper_right
                elif meta == "llp":
                    tr.fillcolor = figure_theme.zone_lower_left
                elif meta == "lrp":
                    tr.fillcolor = figure_theme.zone_lower_right
                elif meta == "lxa":
                    tr.fillcolor = figure_theme.zone_lower_axis
            # Hide borders for polygons
            if hasattr(tr, "line") and tr.line:
                tr.line.color = "rgba(0,0,0,0)"


# ---- Convenience re-exports --------------------------------------------------


def get_palette() -> Palette:
    return PALETTE


def get_typography() -> Typography:
    return TYPO


def get_text_styles() -> Dict[str, Dict[str, str]]:
    """Collects commonly used text styles for import convenience."""
    return {
        "h1": text.h1,
        "h2": text.h2,
        "h3": text.h3,
        "p": text.p,
        "muted": text.muted,
        "small": text.small,
        "code_block": text.code_block,
    }

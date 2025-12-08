from __future__ import annotations

from typing import Dict

from dash import dcc, html, callback, Input, Output

from src.app.style.components.layout import (
    content_wrapper,
    section_card,
    graph_container,
)
from src.app.style.text import TEXT
from src.app.style.palette import PALETTE
from src.app.style.typography import TYPOGRAPHY


def _slugify(page_key: str) -> str:
    """
    Very small slugifier: lowercase + replace spaces/underscores with hyphens
    and strip leading/trailing hyphens. Meant to keep IDs simple and stable.
    """
    slug = (page_key or "page").lower().replace("_", "-").replace(" ", "-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-") or "page"


def stability_ids(page_key: str) -> Dict[str, str]:
    """
    Provide normalized IDs for the three standard placeholders on a stability page.
    """
    slug = _slugify(page_key)
    return {
        "graph": f"ph-{slug}-graph",
        "phase": f"ph-{slug}-phase",
        "explication": f"ph-{slug}-explication",
    }


def build_stability_layout(page_key: str, layout_pedagogic_fn=None) -> html.Div:
    """
    Create a minimal base layout for stability pages with three sections:
    - Graphique interactif (dcc.Graph)
    - Diagramme de phase (dcc.Graph)
    - Explication pédagogique (html.Div)

    The function only provides the strict necessary placeholders, keeping code simple.
    If layout_pedagogic_fn is provided, it will be used to populate the pedagogic section directly.
    """
    ids = stability_ids(page_key)
    title = page_key.replace("_", " ").title()

    # Determine pedagogic content
    pedagogic_content = html.Div(["à compléter"])
    if layout_pedagogic_fn is not None:
        pedagogic_content = layout_pedagogic_fn()

    # Back link style
    back_link_style = {
        "display": "inline-block",
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
    }

    return html.Div(
        [
            # Back link to Poincaré
            html.Div(
                [
                    html.A(
                        "← Retour au diagramme de Poincaré",
                        href="/poincare",
                        style=back_link_style,
                    )
                ],
                style={"marginBottom": "16px"},
            ),
            # Title
            html.H2(title, style=TEXT["h2"]),
            # Section: Graphique interactif
            html.Div(
                [
                    html.H3("Graphique interactif", style=TEXT["h3"]),
                    dcc.Graph(id=ids["graph"]),
                ],
                style={**section_card(), "marginBottom": "20px"},
            ),
            # Section: Diagramme de phase
            html.Div(
                [
                    html.H3("Diagramme de phase", style=TEXT["h3"]),
                    dcc.Graph(id=ids["phase"]),
                ],
                style={**section_card(), "marginBottom": "20px"},
            ),
            # Section: Explication pédagogique
            html.Div(
                [
                    html.H3("Explication pédagogique", style=TEXT["h3"]),
                    html.Div(pedagogic_content, id=ids["explication"], style=TEXT["p"]),
                ],
                style=section_card(),
            ),
        ],
        style=content_wrapper(),
    )

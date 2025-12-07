from __future__ import annotations

from typing import Dict

from dash import dcc, html


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
    title = page_key.capitalize()

    # Determine pedagogic content
    pedagogic_content = html.Div(["à compléter"])
    if layout_pedagogic_fn is not None:
        pedagogic_content = layout_pedagogic_fn()

    return html.Div(
        [
            html.H2(title),
            html.Div(
                [
                    html.H3("Graphique interactif"),
                    dcc.Graph(id=ids["graph"]),
                ],
                style={"marginTop": "12px"},
            ),
            html.Div(
                [
                    html.H3("Diagramme de phase"),
                    dcc.Graph(id=ids["phase"]),
                ],
                style={"marginTop": "12px"},
            ),
            html.Div(
                [
                    html.H3("Explication pédagogique"),
                    html.Div(pedagogic_content, id=ids["explication"]),
                ],
                style={"marginTop": "12px"},
            ),
        ],
        style={"padding": "24px"},
    )

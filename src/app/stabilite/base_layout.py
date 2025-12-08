from __future__ import annotations

from typing import Dict

from dash import Input, Output, callback, dcc, html

from src.app.style.components.layout import (content_wrapper, graph_container,
                                             section_card)
from src.app.style.palette import PALETTE
from src.app.style.text import TEXT
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
    Provide normalized IDs for the standard placeholders on a stability page.
    """
    slug = _slugify(page_key)
    return {
        "graph": f"ph-{slug}-graph",
        "system_graph": f"ph-{slug}-system-graph",
        "phase": f"ph-{slug}-phase",
        "explication": f"ph-{slug}-explication",
        "eigenvalue_display": f"ph-{slug}-eigenvalue-display",
        "ode_display": f"ph-{slug}-ode-display",
    }


def build_stability_layout(
    page_key: str,
    layout_pedagogic_fn=None,
    tau: float = 0.0,
    delta: float = 0.0,
) -> html.Div:
    """
    Create a base layout for stability pages (static display).

    - Affiche les valeurs propres calculées
    - Diagramme de phase (dcc.Graph)
    - Explication pédagogique (html.Div)

    Args:
        page_key: Unique identifier for the page
        layout_pedagogic_fn: Function returning pedagogical content
        tau: Trace value for this equilibrium type
        delta: Determinant value for this equilibrium type
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
            # Section: Paramètres du système
            html.Div(
                [
                    html.H3("Paramètres du système", style=TEXT["h3"]),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Strong(
                                        "Trace (τ) : ", style={"color": PALETTE.text}
                                    ),
                                    html.Span(
                                        f"τ = {tau:.2f}",
                                        style={
                                            "color": PALETTE.primary,
                                            "fontWeight": "bold",
                                        },
                                    ),
                                ],
                                style={"marginBottom": "0.5rem"},
                            ),
                            html.Div(
                                [
                                    html.Strong(
                                        "Déterminant (Δ) : ",
                                        style={"color": PALETTE.text},
                                    ),
                                    html.Span(
                                        f"Δ = {delta:.2f}",
                                        style={
                                            "color": PALETTE.primary,
                                            "fontWeight": "bold",
                                        },
                                    ),
                                ],
                                style={"marginBottom": "0.5rem"},
                            ),
                            html.Div(
                                [
                                    html.Strong(
                                        "Équation différentielle : ",
                                        style={"color": PALETTE.text},
                                    ),
                                ],
                                style={"marginBottom": "0.5rem"},
                            ),
                            html.Div(
                                id=ids["ode_display"],
                                style={
                                    "padding": "12px",
                                    "backgroundColor": PALETTE.bg,
                                    "borderRadius": "8px",
                                    "border": f"1px solid {PALETTE.border}",
                                    "marginTop": "0.5rem",
                                    "marginBottom": "1rem",
                                    "fontFamily": "monospace",
                                    "fontSize": "0.9rem",
                                },
                            ),
                            html.Div(
                                id=ids["eigenvalue_display"],
                                style={
                                    "padding": "12px",
                                    "backgroundColor": PALETTE.bg,
                                    "borderRadius": "8px",
                                    "border": f"1px solid {PALETTE.border}",
                                    "marginTop": "1rem",
                                },
                            ),
                        ],
                    ),
                ],
                style={**section_card(), "marginBottom": "20px"},
            ),
            # Section: Graphe temporel du système
            html.Div(
                [
                    html.H3("Évolution temporelle", style=TEXT["h3"]),
                    html.P(
                        "Trajectoires x₁(t) et x₂(t) montrant l'évolution du système dans le temps.",
                        style=TEXT["muted"],
                    ),
                    dcc.Graph(id=ids["system_graph"]),
                ],
                style={**section_card(), "marginBottom": "20px"},
            ),
            # Section: Diagramme de phase
            html.Div(
                [
                    html.H3("Diagramme de phase", style=TEXT["h3"]),
                    html.P(
                        "Portrait de phase montrant les trajectoires du système dynamique.",
                        style=TEXT["muted"],
                    ),
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
